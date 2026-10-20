---
doc_id: "16"
title: "Test Strategy"
status: "draft"
owner: "QA Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["01_PRD.md", "04_SECURITY_PIPELINE.md", "06_API_CONTRACT.md", "09_ATTACK_TESTS.md"]
---

# Test Strategy

## Test pyramid
- **Unit:** policy classifier, schema validation, state transitions, redaction, approval digest.
- **Integration:** database, MCP transport, model adapter, repository provider, AWS adapter.
- **Contract:** tool schemas, endpoint responses, errors, protocol interoperability.
- **End-to-end:** issue intake through plan, approval, sandbox change, tests, and evidence.
- **Security:** prompt injection, approval replay, scope mismatch, secret canaries, sandbox limits.
- **Accessibility:** keyboard, focus, labels, status announcements, contrast, reduced motion.

## Test data
Use synthetic issues, disposable repositories, test credentials, and sandbox AWS resources. Never run destructive tests against personal or production repositories.

## Required scenarios
- Valid issue; invalid issue URL; inaccessible repository.
- Empty retrieval and conflicting source excerpts.
- Plan-only run does not write files or remote resources.
- Approval granted, denied, expired, and invalidated by parameter change.
- Tool timeout and provider rate limit.
- Tests pass, tests fail, and tests not run.
- MCP client disconnect/reconnect.
- AWS credentials missing or scope denied.
- Open-source evidence URL invalid or status stale.

## Result reporting
Store test name, build/commit, environment, timestamp, status, output artifact, and known limitation. A test is `passed` only when assertions pass; skipped tests must remain `skipped`.

## Release gate
No unresolved critical security finding. All demo-critical paths have automated or documented manual checks. The known-good build is pinned to a commit.
