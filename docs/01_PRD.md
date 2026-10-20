---
doc_id: "01"
title: "Product Requirements Document"
status: "baseline"
owner: "Product Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["00_START_HERE.md"]
---

# Product Requirements Document

## 1. Summary
SDE Agent is a permission-aware engineering workflow agent. It connects developer tools through MCP and helps a developer investigate an issue, assemble source-linked context, propose a plan, prepare a change, run checks, and open a draft pull request. Humans retain control over consequential operations.

## 2. Problem
Engineering tasks require context switching between issue trackers, repositories, CI output, code review, and team communication. General-purpose chat can suggest code, but does not by itself provide a controlled, auditable path from issue to verified change.

## 3. Users
- **Primary:** developer resolving a repository issue.
- **Secondary:** reviewer deciding whether to authorize a proposed operation.
- **Operator:** project owner configuring tool access, policy, and audit retention.
- **Judge/demo viewer:** needs a short, reproducible demonstration of working integrations.

## 4. Goals
- Turn a repository issue into a reviewable, evidence-backed plan.
- Make each tool action and its permission boundary visible.
- Require action-specific approval for remote writes and privileged operations.
- Report actual test and CI outcomes without overstating confidence.
- Demonstrate a working MCP integration and honest Alexa+ simulation.
- Include a real AWS integration and a verifiable open-source contribution.

## 5. Non-goals
- Fully autonomous production deployment.
- Automatic merge without human review.
- Unrestricted shell access or arbitrary tool execution.
- Claiming live Alexa+ functionality where only a web simulation exists.
- Building a separate product for either mini-challenge.

## 6. Primary workflow
Issue intake → retrieve context → build plan → review plan → approve exact action → execute in sandbox → run checks → inspect evidence → prepare draft PR → record audit trail.

## 7. Functional requirements
- FR-01: accept an issue URL or issue identifier and repository.
- FR-02: display source-linked context and distinguish facts from generated analysis.
- FR-03: produce a plan with files/actions, expected effect, risk, and acceptance criteria.
- FR-04: support plan-only mode without code modification.
- FR-05: bind approvals to exact action parameters and expire stale approvals.
- FR-06: enforce tool allowlists, scoped credentials, and execution limits server-side.
- FR-07: display stdout, stderr, exit code, test counts, and relevant logs.
- FR-08: retain timeline events for approvals, tool calls, failures, and outputs.
- FR-09: provide MCP tools over Streamable HTTP and document Agent Skills.
- FR-10: show real AWS integration evidence and a separate open-source contribution record.

## 8. Non-functional requirements
Security by default; responsive interface; keyboard accessibility; reproducible local setup; structured logs; bounded timeouts; useful failure states; secrets redaction; deterministic demo path.

## 9. Success measures
- A judge can complete the demo without undocumented manual steps.
- Every remote write in the demo has a matching approval record.
- Test results shown in the UI match actual command output.
- Track claims map to working features and external evidence.
- A fresh clone can follow setup instructions successfully.

## 10. Open questions
Confirm issue tracker, repository provider, execution sandbox, model provider, AWS service, open-source target repository, and hackathon submission requirements.
