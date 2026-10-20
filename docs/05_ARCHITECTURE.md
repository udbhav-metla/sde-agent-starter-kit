---
doc_id: "05"
title: "System Architecture"
status: "baseline"
owner: "Technical Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["01_PRD.md", "02_THREAT_MODEL.md"]
---

# System Architecture

## 1. Logical components
- **Web client:** investigation intake, run timeline, approvals, evidence, connection management.
- **API/backend:** authentication, orchestration, policy checks, state transitions, audit writes.
- **Agent orchestrator:** planning, context assembly, tool selection, bounded execution loop.
- **MCP adapter:** typed tool registry and Streamable HTTP transport.
- **Agent Skills layer:** reusable, documented task instructions and workflow entry points.
- **Execution sandbox:** isolated workspace for edits and tests.
- **Integrations:** issue/repository provider, CI, communication tool, and selected AWS service.
- **Persistence:** run metadata, approval records, tool events, evidence pointers.
- **Model provider:** configurable provider behind a narrow adapter.

## 2. High-level flow
Browser → API → orchestrator → context/retrieval → plan → policy gate → approval service → sandbox/MCP tool → verification → audit/evidence → UI.

## 3. Architecture constraints
- The UI is never the security boundary.
- The model cannot directly call arbitrary shell or remote APIs.
- MCP tools expose narrow, typed capabilities.
- Each integration has independent credentials and scopes.
- Run state is persisted so refreshes do not invent or lose status.
- Long-running work is asynchronous and cancellable where safe.
- All tool results carry source and execution metadata.

## 4. Suggested deployment shape
For the hackathon, use a small web frontend and one backend service, plus a worker only if asynchronous tasks require it. Run local services with Compose when useful. Keep secrets in environment variables for local development and a managed secret store for deployed environments. Avoid premature microservices.

## 5. State model
`created → collecting_context → planning → awaiting_approval → executing → verifying → completed`
Terminal alternatives: `denied`, `failed`, `cancelled`, `blocked`, `partial`.

## 6. Reliability
Use request IDs, idempotency for supported writes, bounded retries, timeouts, cancellation, and explicit partial-success states. A provider timeout must not be shown as a successful action.

## 7. Architecture decisions to record
Frontend framework, backend framework, database, queue strategy, model provider, repository provider, sandbox technology, MCP server location, and AWS service. Record each decision and its rationale in `19_DECISIONS_AND_ASSUMPTIONS.md`.
