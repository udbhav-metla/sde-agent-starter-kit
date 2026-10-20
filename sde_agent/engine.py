import difflib
import time
from concurrent.futures import ThreadPoolExecutor
from .providers import GitHub, DEMO_FILES, bedrock_plan
from .sandbox import run_checks
from .security import Fault, digest, redact, safe_path, scoped
from .store import Store, uid


class Engine:
    def __init__(self, settings):
        self.settings = settings
        settings.data_dir.mkdir(parents=True, exist_ok=True)
        self.clean = lambda x: redact(x, (settings.token, settings.github_token))
        self.store = Store(settings.data_dir / 'sde.sqlite3', self.clean)
        self.github = GitHub(settings)
        self.pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix='sde')

    def update(self, run, **fields):
        with self.store.lock:
            saved = self.store.get('runs', run['id'])
            if saved['state'] == 'cancelled' and fields.get('state') != 'cancelled':
                raise Fault('CANCELLED', 'Run cancelled.', 409)
            run.update(fields, updated=time.time())
            self.store.put('runs', run)

    def create(self, repository, issue_url, mode, constraints):
        scoped(repository, self.settings)
        if mode not in ('plan_only', 'prepare_change'):
            raise Fault('INVALID_INPUT', 'Unknown execution mode.')
        with self.store.lock:
            if sum(r['state'] in ('collecting_context', 'planning', 'executing', 'verifying') for r in self.store.list('runs')) >= 2:
                raise Fault('RATE_LIMITED', 'Two runs are active; wait for one to finish.', 429)
            run = dict(id=uid(), repository=repository, issue_url=issue_url, mode=mode, constraints=constraints, state='collecting_context', created=time.time(), updated=time.time(), evidence=[], plan=None, context=None, error=None)
            self.store.put('runs', run)
            self.store.event(run['id'], 'run_created', 'Investigation created', repository=repository, mode=mode)
            self.pool.submit(self._collect, run['id'])
            return run

    def _guard(self, id, operation):
        try:
            operation()
        except Exception as exc:
            with self.store.lock:
                r = self.store.get('runs', id)
                if r['state'] == 'cancelled':
                    return
                msg = exc.message if isinstance(exc, Fault) else 'Operation failed unexpectedly; no success claimed.'
                code = exc.code if isinstance(exc, Fault) else 'INTERNAL_ERROR'
                # Protected writes may have produced partial remote side effects.
                self.update(r, state='partial' if r.get('remote_started') else 'failed', error=msg)
                self.store.event(id, 'run_failed', msg, error_code=code)

    def _collect(self, id):
        def operation():
            r = self.store.get('runs', id)
            context = self.clean(self.github.context(r['repository'], r['issue_url']))
            with self.store.lock:
                r = self.store.get('runs', id)
                if r['state'] == 'cancelled':
                    return
                self.update(r, context=context, title=context['title'], state='planning')
                self.store.event(id, 'source_retrieved', f"Read issue and {len(context['files'])} Python files", source=context['url'], commit=context['commit'], trust='untrusted', simulated=context['simulated'])
                if context['simulated']:
                    plan = dict(summary='Guard the empty-list edge case before indexing.', steps=['Inspect the empty and non-empty input behavior.', 'Return None when the input is empty.', 'Run the three regression tests before and after the patch.'], acceptance=['Empty list returns None.', 'Non-empty input preserves its first element, including zero.'], changes=[dict(path='handler.py', before=DEMO_FILES['handler.py'], after='def first_item(items):\n    if not items:\n        return None\n    return items[0]\n')], generated_by='deterministic demonstration fixture')
                    self._set_plan(r, plan)
                else:
                    self.propose(r, 'bedrock_plan', {'model': self.settings.model_id, 'region': self.settings.region, 'context_digest': digest(context), 'constraints': r['constraints'], 'max_output_tokens': 4096}, 'Send the displayed source context to Amazon Bedrock and generate one plan. May incur inference charges.', 'cost-sensitive')
        self._guard(id, operation)

    def _set_plan(self, r, plan):
        if not isinstance(plan, dict) or not isinstance(plan.get('summary'), str) or not isinstance(plan.get('steps'), list) or not all(isinstance(x, str) for x in plan['steps']) or not isinstance(plan.get('acceptance'), list) or not all(isinstance(x, str) for x in plan['acceptance']):
            raise Fault('EXECUTION_FAILED', 'Invalid plan structure.', 422)
        changes = plan.get('changes', [])
        if not isinstance(changes, list) or not 1 <= len(changes) <= 5:
            raise Fault('POLICY_DENIED', 'A plan must change between one and five files.', 403)
        seen = set()
        for c in changes:
            if not isinstance(c, dict) or set(c) != {'path', 'before', 'after'} or not all(isinstance(v, str) for v in c.values()):
                raise Fault('EXECUTION_FAILED', 'Invalid change schema.', 422)
            path = safe_path(c['path'])
            if path in seen or not path.endswith('.py') or any('test' in part.lower() for part in path.split('/')):
                raise Fault('POLICY_DENIED', 'Only unique non-test Python files may be changed.', 403)
            seen.add(path)
            if c['before'] != r['context']['files'].get(path) or len(c['after'].encode()) > 24000 or c['after'] == c['before']:
                raise Fault('POLICY_DENIED', 'Patch is stale, empty, or exceeds the file size limit.', 403)
            if self.clean(c['after']) != c['after']:
                raise Fault('POLICY_DENIED', 'Patch contains secret-like material.', 403)
        diff = '\n'.join(''.join(difflib.unified_diff(c['before'].splitlines(True), c['after'].splitlines(True), fromfile='a/' + c['path'], tofile='b/' + c['path'])) for c in changes)
        self.update(r, plan=plan, diff=diff)
        self.store.event(r['id'], 'plan_generated', 'Plan and exact diff ready for review', generated_by=plan.get('generated_by', 'Amazon Bedrock; untrusted model output'))
        if r['mode'] == 'plan_only':
            self.update(r, state='completed', result='Plan only. No code was changed and no tests were executed.')
        else:
            self.propose(r, 'prepare_change', {'plan_digest': digest(plan), 'source_commit': r['context']['commit'], 'changes': changes, 'test_command': 'python -I -B -m unittest discover -s /workspace -v'}, 'Apply this exact diff in a disposable workspace and execute the fixed test command before and after.', 'local reversible')

    def propose(self, r, tool, parameters, reason, risk):
        action = dict(tool=tool, repository=r['repository'], run_id=r['id'], parameters=parameters)
        approval = dict(id=uid(), run_id=r['id'], actor='local-operator', action=action, digest=digest(action), created=time.time(), expires=time.time() + self.settings.approval_seconds, state='pending', reason=reason, risk=risk)
        self.store.put('approvals', approval)
        self.update(r, state='awaiting_approval', approval_id=approval['id'])
        self.store.event(r['id'], 'approval_requested', reason, approval_id=approval['id'], action_digest=approval['digest'], action=action, risk=risk)
        return approval

    def decide(self, id, decision, action_digest):
        with self.store.lock:
            a = self.store.get('approvals', id)
            r = self.store.get('runs', a['run_id'])
            if a['state'] != 'pending' or r['state'] != 'awaiting_approval' or r.get('approval_id') != id:
                raise Fault('POLICY_DENIED', 'Approval is no longer actionable.', 409)
            if time.time() >= a['expires']:
                a['state'] = 'expired'
                self.store.put('approvals', a)
                self.update(r, state='blocked', error='Approval expired. Start a new investigation.')
                self.store.event(r['id'], 'approval_expired', 'No action executed', approval_id=id)
                raise Fault('APPROVAL_EXPIRED', 'Approval expired.', 409)
            if action_digest != a['digest'] or digest(a['action']) != a['digest']:
                raise Fault('POLICY_DENIED', 'Action parameters do not match the approval.', 403)
            if decision not in ('approve', 'deny'):
                raise Fault('INVALID_INPUT', 'Decision must be approve or deny.')
            scoped(r['repository'], self.settings)
            a.update(state='executing' if decision == 'approve' else 'denied', decided=time.time())
            self.store.put('approvals', a)
            self.update(r, state='executing' if decision == 'approve' else 'denied')
            self.store.event(r['id'], 'approval_' + ('approved' if decision == 'approve' else 'denied'), 'Action approved' if decision == 'approve' else 'Action not approved. Nothing executed for this request.', approval_id=id, action_digest=a['digest'])
            if decision == 'approve':
                self.pool.submit(self._execute, id)
            return a

    def _execute(self, id):
        a = self.store.get('approvals', id)
        def operation():
            r = self.store.get('runs', a['run_id'])
            if r['state'] == 'cancelled':
                return
            scoped(r['repository'], self.settings)
            if a['state'] != 'executing' or digest(a['action']) != a['digest'] or a['actor'] != 'local-operator':
                raise Fault('POLICY_DENIED', 'Invalid execution authorization.', 403)
            if time.time() >= a['expires']:
                raise Fault('APPROVAL_EXPIRED', 'Approval expired before execution began.', 409)
            tool, p = a['action']['tool'], a['action']['parameters']
            self.store.event(r['id'], 'tool_started', tool, approval_id=id, action_digest=a['digest'])
            if tool == 'bedrock_plan':
                if p['context_digest'] != digest(r['context']) or p['model'] != self.settings.model_id or p['region'] != self.settings.region:
                    raise Fault('POLICY_DENIED', 'Model configuration or context changed.', 403)
                plan, aws = bedrock_plan(self.settings, r['context'], r['constraints'])
                self._checkpoint(r['id'])
                r = self.store.get('runs', r['id'])
                r['evidence'].append(dict(kind='aws', **aws))
                self.store.event(r['id'], 'aws_call_completed', 'Bedrock returned a plan', **aws)
                self._set_plan(r, self.clean(plan))
            elif tool == 'prepare_change':
                if p['plan_digest'] != digest(r['plan']) or p['source_commit'] != r['context']['commit'] or p['changes'] != r['plan']['changes']:
                    raise Fault('POLICY_DENIED', 'Plan or source changed since approval.', 403)
                files = r['context']['files'].copy()
                fixture = r['repository'] == 'demo/empty-input' and files == DEMO_FILES and r['plan']['changes'] == [{'path': 'handler.py', 'before': DEMO_FILES['handler.py'], 'after': 'def first_item(items):\n    if not items:\n        return None\n    return items[0]\n'}]
                cancel = lambda: self.store.get('runs', r['id'])['state'] == 'cancelled'
                baseline = run_checks(self.settings, files, fixture, cancel)
                self._checkpoint(r['id'])
                r = self.store.get('runs', r['id'])
                r['evidence'].append(dict(kind='tests_before', **baseline))
                self.store.event(r['id'], 'tests_completed', 'Baseline tests completed', exit_code=baseline['exit_code'], tests=baseline['tests'], passed=baseline['passed'])
                for change in p['changes']:
                    files[change['path']] = change['after']
                self.update(r, state='verifying')
                after = run_checks(self.settings, files, fixture, cancel)
                self._checkpoint(r['id'])
                r = self.store.get('runs', r['id'])
                r['evidence'].append(dict(kind='tests_after', **after))
                r['evidence'].append(dict(kind='diff', content=r['diff'], digest=digest(p['changes'])))
                self.update(r, state='completed' if after['passed'] else 'failed', result='Tests passed; inspect the diff and acceptance criteria.' if after['passed'] else 'Verification failed or no tests were discovered.', verified_patch_digest=digest(p['changes']) if after['passed'] else None)
                self.store.event(r['id'], 'tests_completed', r['result'], exit_code=after['exit_code'], tests=after['tests'], passed=after['passed'])
            elif tool == 'create_draft_pull_request':
                if not r.get('verified_patch_digest') or digest(p['changes']) != r['verified_patch_digest']:
                    raise Fault('POLICY_DENIED', 'Draft PR requires the exact tested patch.', 403)
                self._checkpoint(r['id'])
                with self.store.lock:
                    r = self.store.get('runs', r['id'])
                    if r['state'] == 'cancelled':
                        return
                    self.update(r, remote_started=True)
                pr = self.github.publish(r['repository'], p)
                r = self.store.get('runs', r['id'])
                r['evidence'].append(dict(kind='draft_pull_request', url=pr['html_url'], number=pr['number']))
                self.update(r, state='completed', pr_url=pr['html_url'])
                self.store.event(r['id'], 'draft_pr_created', 'Draft pull request created', url=pr['html_url'])
            else:
                raise Fault('POLICY_DENIED', 'Unknown protected tool.', 403)
            a['state'] = 'succeeded'
            self.store.put('approvals', a)
            self.store.event(r['id'], 'tool_completed', tool, approval_id=id, outcome='succeeded')
        self._guard(a['run_id'], operation)
        a = self.store.get('approvals', id)
        if a['state'] == 'executing':
            a['state'] = 'failed'
            self.store.put('approvals', a)

    def _checkpoint(self, id):
        if self.store.get('runs', id)['state'] == 'cancelled':
            raise Fault('CANCELLED', 'Run cancelled.', 409)

    def cancel(self, id):
        with self.store.lock:
            r = self.store.get('runs', id)
            if r.get('remote_started'):
                raise Fault('POLICY_DENIED', 'Remote write already started; inspect its result before further action.', 409)
            if r['state'] in ('completed', 'failed', 'denied', 'cancelled', 'partial'):
                raise Fault('POLICY_DENIED', 'Run has already stopped.', 409)
            self.update(r, state='cancelled')
            self.store.event(id, 'cancellation_requested', 'Cancellation requested. In-flight reads may finish; no new action will start.')
            return r

    def draft(self, id):
        with self.store.lock:
            r = self.store.get('runs', id)
            scoped(r['repository'], self.settings)
            if not self.settings.github_write or not self.settings.github_token or r['repository'] == 'demo/empty-input':
                raise Fault('SCOPE_MISMATCH', 'Configure a real GitHub repository and enable SDE_GITHUB_WRITE.', 403)
            if r['state'] != 'completed' or not r.get('verified_patch_digest') or r.get('remote_started'):
                raise Fault('POLICY_DENIED', 'Draft PR requires a completed verified change with no prior publication attempt.', 409)
            p = dict(base_commit=r['context']['commit'], base_branch=r['context']['branch'], branch='sde/fix-' + id[:12], title='Fix: ' + r['title'][:120], body='## Problem\n' + r['issue_url'] + '\n\n## Change\n' + r['plan']['summary'] + '\n\n## Validation\nAllowlisted unittest command passed in an isolated container. Review recorded evidence and acceptance criteria.\n\nPrepared by SDE Agent; human review required.', changes=r['plan']['changes'])
            return self.propose(r, 'create_draft_pull_request', p, 'Create Git objects, a new branch, and one draft pull request with the exact tested patch. No merge.', 'remote write')

    def close(self):
        self.pool.shutdown(wait=True, cancel_futures=True)
        self.github.client.close()
        self.store.db.close()
