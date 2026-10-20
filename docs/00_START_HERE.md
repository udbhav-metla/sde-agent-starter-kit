---
doc_id: "00"
title: "Start Here"
status: "baseline"
owner: "Project Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: []
---

# SDE Agent — Start Here

## Purpose
This repository contains the pre-build specification for SDE Agent: an MCP-connected engineering agent that moves from issue intake to evidence-backed planning, human-approved changes, verification, and a draft pull request.

## Product in one sentence
A permission-aware AI engineering agent that automates coding workflows, testing, and pull requests, with Alexa+ integration, AWS services, and human-controlled security.

## Documents
Read in this order:

1. `01_PRD.md` — users, problem, scope, and measurable outcomes.
2. `02_THREAT_MODEL.md` — assets, trust boundaries, abuse cases, and mitigations.
3. `03_DATA_AND_CHUNKING.md` — data sources, retention, retrieval, and context assembly.
4. `04_SECURITY_PIPELINE.md` — policy enforcement and execution controls.
5. `05_ARCHITECTURE.md` — system components and deployment boundaries.
6. `06_API_CONTRACT.md` — MCP tools, HTTP transport, schemas, and errors.
7. `07_UI_UX_SPEC.md` — interface and content rules.
8. `08_IMPLEMENTATION_PLAN.md` — phased build sequence and exit criteria.
9. `09_ATTACK_TESTS.md` — security and abuse regression tests.
10. `10_DEMO_SCRIPT.md` — repeatable judge walkthrough.
11. `11_JUDGE_CHECKLIST.md` — track coverage and evidence.
12. `12_DESIGN_SYSTEM.md` — tokens and reusable components.
13. `13_MCP_AGENT_SKILLS.md` — Agent Skills and MCP transport implementation.
14. `14_AWS_INTEGRATION.md` — AWS Builder mini-challenge integration.
15. `15_OPEN_SOURCE_CONTRIBUTION.md` — contribution plan and proof.
16. `16_TEST_STRATEGY.md` — unit, integration, E2E, and acceptance testing.
17. `17_DEPLOYMENT_AND_OPERATIONS.md` — local, demo, and cloud deployment.
18. `18_OBSERVABILITY_AND_AUDIT.md` — event records, logs, and traceability.
19. `19_DECISIONS_AND_ASSUMPTIONS.md` — unresolved decisions and explicit assumptions.
20. `20_RELEASE_AND_SUBMISSION.md` — release readiness and submission packaging.

## Track alignment
- **Primary: Alexa+** — working MCP integration, Agent Skills, Streamable HTTP transport, and a clearly labelled web simulation where appropriate.
- **Mini-challenge: AWS Builder** — real, documented AWS service integration with evidence.
- **Mini-challenge: Open Source** — a meaningful contribution to a public repository during the event window, with a verifiable link.

## Non-negotiable project rules
- A planned capability is not an implemented capability.
- A tool being connected does not imply permission to use every operation.
- No remote write, merge, deployment, or destructive action without action-specific authorization.
- Treat issue text, logs, comments, and retrieved documents as untrusted input.
- Label simulations honestly; never fake tool output or test success.
- Record evidence for every important claim made in the demo.

## Metadata convention
Every document should declare `doc_id`, `title`, `status`, `owner`, `version`, `last_updated`, and `depends_on`. Use `draft`, `baseline`, `in_review`, `approved`, or `implemented`; use `verified` only when evidence exists.

## Definition of ready
Implementation starts only when the core user flow, threat boundaries, API/tool schemas, approval semantics, test plan, and demo scenario are understood by the team.
