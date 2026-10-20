---
doc_id: "10"
title: "Judge Demo Script"
status: "draft"
owner: "Demo Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["01_PRD.md", "07_UI_UX_SPEC.md", "11_JUDGE_CHECKLIST.md", "20_RELEASE_AND_SUBMISSION.md"]
---

# Judge Demo Script

## Demo promise
Show one issue moving through evidence-backed planning, human authorization, real verification, and a draft delivery artifact. Demonstrate AWS and open-source work separately with verifiable evidence.

## Before the demo
- Use a disposable public or demo repository with no private data.
- Confirm MCP endpoint and Agent Skill are working.
- Confirm the AWS integration uses a sandbox account/resource.
- Open the actual open-source issue/PR/commit.
- Reset demo state and remove tokens from terminal history.
- Verify network, model quota, and provider rate limits.

## Walkthrough (target 4–6 minutes)
1. **Problem (30 sec):** open a real issue and describe the manual context switching.
2. **MCP/Skill (45 sec):** show the available skill and tool discovery; retrieve actual issue data.
3. **Evidence (45 sec):** inspect source-linked context and a structured plan.
4. **Approval (45 sec):** show the exact proposed action and risk; approve a sandboxed change or deny a protected operation.
5. **Verification (60 sec):** run tests and show real exit code, counts, and diff.
6. **Delivery (30 sec):** create or show a draft PR only if approved; open its real URL.
7. **AWS Builder (30 sec):** show the actual service, scope, request/result, and artifact/log.
8. **Open Source (30 sec):** show the public repo, contribution, checks, and PR/commit status.

## Narration rules
- Say “simulated” when the Alexa+ interaction is a web simulation.
- Say “planned” when an integration is not implemented.
- Do not claim the patch is correct solely because tests pass.
- Do not show secrets, private repository content, or personal data.
- If a step fails, explain the actual failure and use a documented fallback; do not fake a success state.

## Fallbacks
Prepare screenshots of real outputs only as backup. Label screenshots as captured evidence, not live execution. Have a short recording available if provider availability is uncertain, while keeping the live path honest.
