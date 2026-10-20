---
doc_id: "20"
title: "Release and Submission Readiness"
status: "draft"
owner: "Release/Submission Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["08_IMPLEMENTATION_PLAN.md", "09_ATTACK_TESTS.md", "10_DEMO_SCRIPT.md", "11_JUDGE_CHECKLIST.md", "14_AWS_INTEGRATION.md", "15_OPEN_SOURCE_CONTRIBUTION.md", "17_DEPLOYMENT_AND_OPERATIONS.md"]
---

# Release and Submission Readiness

## 1. Release candidate
Record repository URL, commit SHA, build date, environment, model/provider configuration, and known limitations. Use one pinned build for final judging.

## 2. Submission contents
- Project summary and architecture.
- Setup instructions and environment variable template.
- MCP endpoint and Agent Skills instructions.
- Demo script and short fallback recording/screenshots if permitted.
- Security model and approval behavior.
- AWS integration description and evidence.
- Open-source contribution URL and status.
- Test results, known issues, and limitations.
- Attribution, licenses, and third-party service disclosures.

## 3. Final checks
- [ ] Fresh clone and setup work.
- [ ] No secrets in repository, logs, screenshots, or demo.
- [ ] MCP transport and at least one useful tool are verified.
- [ ] Alexa+ simulation is labelled accurately.
- [ ] Approval and denial paths are both demonstrated.
- [ ] Test output matches actual execution.
- [ ] AWS integration is real and evidence is available.
- [ ] Open-source contribution link is public and accurate.
- [ ] Accessibility and attack-test gates are reviewed.
- [ ] README claims match implemented behavior.
- [ ] Demo fallback is captured from real output and labelled.

## 4. Submission evidence index
| Claim | Evidence URL/path | Verified by | Date | Status |
|---|---|---|---|---|
| MCP tool works | TBD | TBD | TBD | Not verified |
| Agent Skill works | TBD | TBD | TBD | Not verified |
| Approval gate blocks denial | TBD | TBD | TBD | Not verified |
| Test results are real | TBD | TBD | TBD | Not verified |
| AWS integration works | TBD | TBD | TBD | Not verified |
| Open-source contribution exists | TBD | TBD | TBD | Not verified |

## 5. Honest release language
Use `implemented` for shipped behavior, `verified` only when evidence is recorded, and `planned` for future work. Do not describe an open PR as merged, a mock as live, or a passing test suite as proof of total correctness.
