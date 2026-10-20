---
doc_id: "02"
title: "Threat Model"
status: "in_review"
owner: "Security Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["01_PRD.md", "05_ARCHITECTURE.md"]
---

# Threat Model

## 1. Security objective
Prevent untrusted issue content, model output, or tool responses from causing unauthorized actions or misleading users about what occurred.

## 2. Assets
- Repository source and write permissions
- GitHub/AWS tokens and other secrets
- User issues, comments, code, logs, and retrieved documents
- Approval records and audit events
- CI credentials and generated artifacts
- User identity, project configuration, and integration scopes

## 3. Trust boundaries
1. Browser ↔ backend API
2. Backend ↔ model provider
3. Backend ↔ MCP client/server and remote tools
4. Agent planner ↔ policy enforcement layer
5. Orchestrator ↔ shell/container sandbox
6. Application ↔ Git provider and CI
7. Application ↔ AWS account/services
8. Untrusted repository content ↔ system instructions

## 4. Threat actors and abuse cases
- Malicious issue author embeds prompt injection in issue text.
- Repository file instructs the agent to exfiltrate environment variables.
- Tool result includes hostile instructions or forged success text.
- Stolen token is used beyond the intended repository or scope.
- Approval is replayed after the target or parameters have changed.
- Shell command attempts network access, persistence, or secret discovery.
- A compromised dependency alters test output or build artifacts.
- UI shows a model claim as verified tool evidence.
- Demo uses fake AWS or open-source proof that cannot be independently checked.

## 5. Core mitigations
- Treat retrieved content as data, never as policy.
- Keep policy enforcement outside the model.
- Use server-side allowlists and typed tool schemas.
- Default to read-only scopes and least privilege.
- Bind approval to a stable action payload/hash, target, user, and expiry.
- Revalidate policy immediately before execution.
- Run code in an isolated, resource-limited workspace.
- Restrict network egress and mount secrets only when necessary.
- Redact secrets from logs and model context.
- Verify tool responses against structured status and exit codes.
- Record immutable audit events for approval and execution.
- Label mock/simulated actions and results visibly.

## 6. Risk register

| Risk | Likelihood | Impact | Initial control | Verification |
|---|---|---|---|---|
| Prompt injection | High | High | Untrusted-content boundary; action policy | Attack test suite |
| Approval replay | Medium | High | Expiry and action hash | Replay test |
| Secret leakage | Medium | Critical | Secret isolation and redaction | Canary-secret test |
| Unsafe shell command | Medium | Critical | Sandbox and command policy | Denylist/allowlist tests |
| False success display | Medium | High | Tool-grounded state machine | Fault-injection test |
| Over-scoped token | Medium | High | Least-privilege scopes | Permission review |
| AWS cost surprise | Low/Medium | Medium | Budget caps and confirmation | Cost-path review |

## 7. Residual risks
Model interpretation remains probabilistic; sandbox escape and upstream tool compromise cannot be ruled out solely by prompt instructions. Keep sensitive operations human-gated and scope the demo to low-risk resources.

## 8. Security acceptance
No test may pass solely because the model says it complied. Tests must inspect actual side effects, audit records, exit codes, and authorization decisions.
