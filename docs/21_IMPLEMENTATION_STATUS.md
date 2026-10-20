---
doc_id: "21"
title: "Implementation Status and Decisions"
status: "implemented"
owner: "Project owner"
version: "0.1.0"
last_updated: "2026-10-20"
depends_on: ["00_START_HERE.md", "19_DECISIONS_AND_ASSUMPTIONS.md"]
---

# Implementation status

Repository update: the owner requested a new repository after access to the original target could not be established. The organized implementation is now targeted at `udbhav-metla/sde-agent-starter-kit`. The original target and access checks below remain historical records, not the active publication destination.

This file records the built release separately from the original pre-build specifications, which remain unchanged. Read the root README for startup and exact limitations. A local MVP has been implemented; the full hackathon submission is not yet verified.

Verification on 20 October 2026: 32 tests passed (one dependency deprecation warning), official MCP SDK interoperability and reconnect passed using protocol 2025-11-25, browser workflow passed on desktop and mobile, Python compilation passed, and the distributable wheel built successfully. Reports and captured screenshots are under `evidence/`. These are local checks, not evidence of a live AWS call, hosted CI run, actual GitHub PR, or event qualification.

## Decisions taken on 20 October 2026

| Decision | Selection and reason | Consequence |
|---|---|---|
| D-01 Frontend | Browser JavaScript and CSS, matching the documented neutral console | One service, no frontend build runtime; explicit departure from the proposal's suggested Next.js stack |
| D-02 Backend | FastAPI, Pydantic, SQLite WAL, two bounded worker threads | Typed contract and durable local state; one process, one local user |
| D-03 Model | Amazon Bedrock Converse, chosen model and region supplied by operator | One cost/data-transfer approval per call; no implicit cloud usage |
| D-04 Repository | GitHub; user selected `Ashwath-Raj/God-Father-Of-Anton` | Exact allowlist in configuration example; token required for private access |
| D-05 Sandbox | Restricted Docker container for every external repository; exact shipped fixture may run in a subprocess | No external host execution fallback; Docker daemon and image required |
| D-06 AWS | Bedrock is the only AWS integration | Adapter implemented and mocked contract tested; live AWS evidence pending |
| D-07 Open source | No upstream contribution selected or published | Mini-challenge remains open; publishing this project does not satisfy it |
| D-08 Alexa+ | Labelled text simulation with interpreted-request preview | No live Alexa or speech-recognition claim; visual approval remains mandatory |
| D-09 Storage | SQLite local data; retain until explicit operator reset | No automatic retention scheduler; reset after exporting required demo evidence |
| D-10 Submission | Evidence bundle and preserved specifications | Event rules, dates, eligibility and live service proof still need owner validation |

## Requirement coverage

| Requirement | Implementation | Verification |
|---|---|---|
| FR-01 Intake | Scoped repository + issue URL, labelled demo | API and browser checks |
| FR-02 Provenance | Pinned commit, issue URL, file paths, line-level MCP search; untrusted content labels | MCP SDK retrieval and search |
| FR-03 Plan | Summary, steps, acceptance, exact file diff, risk-bearing action | Fixture and structured model-output validation |
| FR-04 Plan only | No execution approval, patch workspace, or tests | Automated test |
| FR-05 Exact approval | Actor, target, immutable action snapshot, SHA-256 digest, ten-minute expiry, single-use decision | Denial, expiry, changed payload, replay tests |
| FR-06 Policy | Local bearer authentication, origin/host checks, repository allowlist, no arbitrary command, fixed execution limits | API and executor tests; real Docker isolation not exercised here |
| FR-07 Test evidence | Actual before/after stdout, stderr, exit, count, duration | Actual fixture subprocess and browser flow |
| FR-08 Audit | Persistent timeline, append-only SQL triggers, hash chain, integrity check | Audit tests and browser check |
| FR-09 MCP/skill | Seven official-SDK tools; stateless Streamable HTTP; reusable skill | Real SDK initialize/discovery/call/reconnect verified; separate skill-host invocation pending |
| FR-10 External proof | GitHub and Bedrock adapters; actual-response evidence schema | Mocked provider contracts; real AWS, draft PR, and public contribution evidence pending |

## Security test mapping

AT-01 and AT-10: injection text cannot authorize a tool; configured token, secret formats, and canaries are redacted. AT-03/04: unknown MCP tool and invalid typed arguments are rejected. AT-05/06: changed and expired approvals fail. AT-07/11: write scope and denied-action checks prevent publication. AT-08: executor timeout is exercised and the subprocess terminates. AT-09: nonzero exit overrides success-shaped text; zero discovered tests cannot count as verification. AT-13: cancellation blocks pending approval and future work. AT-14: approval replay is rejected and a publication attempt cannot be automatically retried.

AT-02 (actual container network escape), AT-12 (actual AWS resource-scope denial), real provider quotas, container resource exhaustion, multi-user access, supply-chain compromise, and live GitHub partial publication have not been verified against external services. Automated provider tests use explicit test doubles. No claim of complete attack resistance is made.

## Public access check for selected repository

On 20 October 2026, unauthenticated GitHub REST requests for the selected repository and its open issues both returned HTTP 404. This can indicate a private repository or unavailable URL; it does not prove that the repository is empty or nonexistent. No issue was selected and no write was attempted. Configure a scoped local token and a real issue URL to continue the live path. Bedrock model/region access has not yet been supplied.

## Release blockers and scope limits

The full documented issue-to-real-draft-PR outcome still requires a reachable target repository containing supported Python code and tests, an actual issue, Bedrock model access, Docker, and action-specific approval in the running app. The supplied source folder itself contains only documentation, so its contents do not provide a runnable Python bug-fix target yet. Building and publishing this console and investigating an issue through the console are distinct workflows.

No deployments, merges, team messages, cloud resources, or upstream open-source PRs were created. The stakeholder update is prepared text only. Local execution, typed transport, policy enforcement, and captured UI/evidence are verified separately from those unfinished external submission gates.
