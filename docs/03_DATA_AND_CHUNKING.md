---
doc_id: "03"
title: "Data Sources and Context Assembly"
status: "draft"
owner: "AI/Backend Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["01_PRD.md", "02_THREAT_MODEL.md", "05_ARCHITECTURE.md"]
---

# Data Sources and Context Assembly

## 1. Purpose
Define which data the agent can retrieve, how it is normalized, what enters model context, and what is retained.

## 2. Data inventory

| Source | Expected data | Trust level | Default access |
|---|---|---|---|
| Issue tracker | Title, description, comments, labels | Untrusted | Read-only |
| Git repository | Files, history, diffs | Untrusted | Read-only until approved |
| CI system | Logs, status, artifacts | Untrusted output | Read-only |
| MCP tool result | Structured result and metadata | External input | Per-tool |
| AWS service | Scoped resource metadata/results | External input | Least privilege |
| User instructions | Task constraints | User-provided | Validate for conflicts |
| Audit store | Actions, approvals, outcomes | Application record | Restricted |

## 3. Context assembly pipeline
1. Validate source URL and repository identity.
2. Fetch only data allowed by the connection scope.
3. Normalize each item with source, timestamp, content type, and stable identifier.
4. Mark retrieved content as untrusted.
5. Remove secrets and irrelevant boilerplate.
6. Rank relevant snippets using lexical or semantic retrieval.
7. Apply token budget and source diversity limits.
8. Include source references beside excerpts.
9. Persist only data needed for run recovery and audit.

## 4. Chunking rules
- Prefer semantic boundaries: issue sections, functions/classes, documentation headings, and log blocks.
- Keep file path, line range, commit/version, and source ID attached to each code chunk.
- Do not split stack traces or structured records mid-entry where avoidable.
- Use overlap only when it improves context continuity; document the chosen overlap.
- Keep code chunks smaller than the model context budget and reserve room for system policy, user request, tool schemas, and output.
- Never merge content from different trust levels without preserving provenance.

## 5. Retrieval requirements
- Retrieval results must include source ID, locator, excerpt, timestamp/version, and confidence/relevance score where available.
- Deduplicate near-identical snippets.
- Prefer current branch/version when investigating a current issue.
- Do not treat retrieval rank as proof of truth.
- If sources conflict, display the conflict instead of silently selecting one.

## 6. Retention and privacy
Define retention duration before implementation. Avoid storing full repositories or secrets unnecessarily. Provide deletion paths for run artifacts where feasible. Do not send data to a model provider unless the configured policy permits it.

## 7. Failure cases
Handle missing permissions, rate limits, stale branches, oversized files, encoding errors, unavailable embeddings, and empty retrieval results. The UI must distinguish “no evidence found” from “source could not be accessed.”

## 8. Acceptance tests
- Every displayed excerpt has provenance.
- Secret canaries do not appear in prompt logs or UI.
- An inaccessible source is reported as inaccessible, not empty.
- Context truncation is recorded and does not silently drop policy instructions.
