---
doc_id: "06"
title: "API and MCP Contract"
status: "draft"
owner: "Backend Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["05_ARCHITECTURE.md", "13_MCP_AGENT_SKILLS.md"]
---

# API and MCP Contract

## 1. Contract principles
Typed inputs, explicit outputs, stable identifiers, predictable errors, bounded execution, and no implicit authorization. Validate every request on the server.

## 2. Core HTTP endpoints (proposed)

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/runs` | Create an investigation run |
| `GET` | `/api/runs/{run_id}` | Retrieve run state and summary |
| `GET` | `/api/runs/{run_id}/events` | Read timeline events |
| `POST` | `/api/runs/{run_id}/plan` | Request or regenerate plan |
| `POST` | `/api/approvals/{approval_id}/decision` | Approve or deny an exact action |
| `GET` | `/api/connections` | List configured connections and scopes |
| `GET` | `/api/runs/{run_id}/evidence` | Retrieve evidence metadata |
| `POST` | `/api/runs/{run_id}/cancel` | Request safe cancellation |

These routes are a proposed baseline, not an implemented contract. Freeze schemas before frontend/backend integration.

## 3. Proposed MCP tools
- `get_issue`: fetch a scoped issue and comments.
- `search_repository`: search files and symbols in an allowed repository.
- `read_file`: read a file at a pinned branch/commit.
- `get_ci_status`: retrieve status and linked logs.
- `propose_change`: produce a patch in the sandbox, not a remote write.
- `run_tests`: execute approved test commands inside the sandbox.
- `create_draft_pull_request`: remote write; approval required.
- `post_status_update`: remote write; approval required.
- `get_aws_resource_status`: only for the AWS service actually integrated.

## 4. Example run request
```json
{
  "issue_url": "https://example.invalid/org/repo/issues/184",
  "repository": "org/repo",
  "mode": "plan_only",
  "constraints": ["Do not change public API"]
}
```

## 5. Common response envelope
```json
{
  "request_id": "req_example",
  "status": "accepted",
  "data": {},
  "error": null
}
```

## 6. Error codes
`INVALID_INPUT`, `UNAUTHENTICATED`, `FORBIDDEN`, `SCOPE_MISMATCH`, `APPROVAL_REQUIRED`, `APPROVAL_EXPIRED`, `POLICY_DENIED`, `TOOL_UNAVAILABLE`, `RATE_LIMITED`, `TIMEOUT`, `EXECUTION_FAILED`, `CANCELLED`, `INTERNAL_ERROR`.

## 7. Streamable HTTP
Document the MCP endpoint URL, authentication method, session behavior, supported protocol version, tool discovery, error mapping, and request limits. Test reconnects and interrupted streams. Do not claim protocol compliance until interoperability tests pass.

## 8. Contract acceptance
Publish JSON schemas, examples, error semantics, approval rules, and a versioning policy. Frontend and backend must use the same schema source.
