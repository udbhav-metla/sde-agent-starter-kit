---
doc_id: "19"
title: "Decisions and Assumptions Register"
status: "in_review"
owner: "Project Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["00_START_HERE.md"]
---

# Decisions and Assumptions Register

Use this register to prevent unspoken assumptions from becoming architecture. Update each item with an owner, date, decision, and rationale.

## Open decisions

| ID | Decision | Options / question | Owner | Status |
|---|---|---|---|---|
| D-01 | Frontend stack | Confirm framework and component library | Frontend Lead | Open |
| D-02 | Backend stack | Confirm API framework and persistence | Backend Lead | Open |
| D-03 | Model provider | Provider, data policy, quotas, fallback | AI Lead | Open |
| D-04 | Repository provider | GitHub or other; scopes and demo repo | Integration Lead | Open |
| D-05 | Sandbox | Container/workspace isolation and egress | Security Lead | Open |
| D-06 | AWS service | Pick one eligible, testable service | Cloud Lead | Open |
| D-07 | Open-source target | Repository and bounded contribution | OSS Lead | Open |
| D-08 | Alexa+ experience | Exact simulation mechanism and label | Product Lead | Open |
| D-09 | Storage/retention | Run state, evidence pointers, retention period | Backend Lead | Open |
| D-10 | Submission evidence | Required links, format, and judging constraints | Submission Lead | Open |

## Assumptions to validate
- The event accepts a web-based Alexa+ simulation for the demo.
- The primary MCP integration can be demonstrated independently of the UI.
- AWS free-tier or sandbox resources are sufficient for the chosen service.
- A public contribution can be completed during the official window.
- The demo can use a disposable repository without sensitive data.
- The team can obtain the required permissions and credentials in time.

## Decision record template
```text
ID:
Date:
Decision:
Context:
Alternatives considered:
Rationale:
Consequences:
Owner:
Evidence / link:
```

Do not mark an assumption confirmed without a source or organizer response. If a decision changes architecture or security, update the dependent documents.
