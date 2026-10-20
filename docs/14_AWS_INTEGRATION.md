---
doc_id: "14"
title: "AWS Builder Integration Plan"
status: "draft"
owner: "Cloud Integration Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["02_THREAT_MODEL.md", "05_ARCHITECTURE.md", "06_API_CONTRACT.md", "11_JUDGE_CHECKLIST.md"]
---

# AWS Builder Integration Plan

## Purpose
Add one meaningful AWS integration to the primary SDE Agent workflow. The AWS mini-challenge extends the same project; it is not a second application.

## Service selection
Choose one service that can be integrated, tested, and explained within the event schedule. Candidate options from the event brief include Amazon Bedrock, AgentCore, Strands SDK, Kiro, and SageMaker. Confirm eligibility and current service requirements before committing.

**Decision pending:** selected service, exact API/SDK, account/region, cost ceiling, and proof artifact.

## Integration requirements
- Describe the engineering problem the service solves.
- Document request/response flow and where the service sits in the architecture.
- Use least-privilege credentials; never commit keys.
- Provide `.env.example` entries without values.
- Define timeouts, quotas, retries, failure states, and cleanup.
- Keep model/service output marked as external input.
- Require approval for remote writes or cost-sensitive operations.
- Link to actual logs, outputs, or artifacts in the demo.

## Evidence record
Record service name, date, environment, request ID (redacted if necessary), action, outcome, artifact link, and cleanup result. Do not publish account IDs, credentials, or sensitive logs.

## Acceptance checklist
- [ ] Integration uses the real selected AWS service.
- [ ] Local/demo configuration is documented.
- [ ] Missing credentials fail clearly.
- [ ] Quota/timeouts are handled.
- [ ] Cost limits and cleanup are documented.
- [ ] At least one reproducible request succeeds.
- [ ] Demo evidence is available.
