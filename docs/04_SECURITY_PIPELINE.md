---
doc_id: "04"
title: "Security Pipeline and Policy Enforcement"
status: "baseline"
owner: "Security/Backend Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["02_THREAT_MODEL.md", "05_ARCHITECTURE.md", "06_API_CONTRACT.md"]
---

# Security Pipeline and Policy Enforcement

## 1. Rule
The model may propose an action; deterministic application code decides whether that action is allowed.

## 2. Request path
Authenticate user → validate request → load policy → classify action → check connection scopes → validate target and parameters → determine approval requirement → request approval if needed → revalidate policy → execute in sandbox/remote tool → validate result → redact output → append audit event.

## 3. Action classes

| Class | Examples | Default handling |
|---|---|---|
| Read-only | Read issue, list files, inspect CI status | Allow if scoped |
| Local reversible | Edit file in isolated workspace | Plan and diff first |
| Remote write | Create branch, comment, draft PR | Explicit approval |
| Privileged/destructive | Merge, deploy, delete resource, broad shell | Deny by default; separate elevated approval if ever supported |

## 4. Enforcement controls
- Tool allowlist and schema validation.
- Repository/resource allowlist.
- Per-run time, token, output, and tool-call limits.
- Command execution in a temporary workspace with resource limits.
- Restricted network egress.
- No ambient credentials inside untrusted code execution.
- Secrets stored in a secret manager or protected environment, not source files.
- Approval bound to exact parameters, target, actor, expiry, and action digest.
- Recheck permissions at execution time.
- Idempotency key for retryable remote writes where supported.
- Rate limits and bounded retries.
- Structured, redacted audit events.

## 5. Approval lifecycle
`proposed → pending → approved/denied/expired → executing → succeeded/failed`

A change to command, repository, branch, target, or meaningful parameters invalidates approval. Denial must result in no execution of the denied action.

## 6. Failure handling
Fail closed for unknown tool names, invalid schemas, missing permission, expired approvals, unrecognized action classes, and policy service failure. Do not automatically retry non-idempotent writes.

## 7. Security acceptance criteria
- No remote write without matching valid approval.
- A denied request has no external side effect.
- Approval replay against changed parameters fails.
- Secrets are redacted from logs and model context.
- Policy enforcement does not depend on model compliance.
