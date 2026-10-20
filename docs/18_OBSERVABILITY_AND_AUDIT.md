---
doc_id: "18"
title: "Observability and Audit"
status: "draft"
owner: "Backend/Operations Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["02_THREAT_MODEL.md", "04_SECURITY_PIPELINE.md", "05_ARCHITECTURE.md"]
---

# Observability and Audit

## Goals
Make the agent's behavior reconstructable: what it attempted, which tools ran, what was approved, what happened, and what evidence supports the displayed status.

## Event fields
- `event_id`, `run_id`, `request_id`, timestamp
- actor and authorization context
- event type and state transition
- tool name and sanitized input summary
- target resource/repository/branch
- approval ID and action digest, where applicable
- start/end time, duration, exit code
- outcome and structured error code
- evidence/artifact references
- redaction markers and schema version

## Events to capture
Run created, source retrieved, plan generated, approval requested/approved/denied/expired, tool started/completed, test started/completed, cancellation requested, artifact created, AWS call completed, contribution record updated, run completed/failed/blocked.

## Logging rules
- Never log raw secrets, authorization headers, private keys, or unredacted sensitive payloads.
- Keep logs structured and searchable.
- Separate agent-generated summary from raw tool evidence.
- Preserve timestamps and stable IDs.
- Limit retention and access to audit records.
- Avoid logging complete source files when a reference and excerpt are sufficient.

## User-visible traceability
The run timeline should link to source evidence, diffs, test output, and pull requests. If evidence is missing, show `Evidence unavailable`; do not synthesize a replacement.

## Acceptance
A reviewer can reconstruct a protected action from proposal through approval and outcome. Every displayed success state maps to a real event or verified artifact.
