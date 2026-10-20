# Documentation map

The numbered specification files preserve the supplied project documentation. Implementation status is recorded separately so the original requirements are not mistaken for completed capabilities.

| Start with | Purpose |
|---|---|
| [Project README](../README.md) | Install, run, configure, and understand current limits |
| [Implementation status](21_IMPLEMENTATION_STATUS.md) | Decisions, requirement coverage, verified behavior, and remaining gates |
| [HTTP contract](api.openapi.json) | Exported FastAPI OpenAPI schema |
| [Operations guide](OPERATIONS.md) | Detailed integration setup, permissions, execution limits, and recovery |
| [Evidence index](../evidence/README.md) | Captured tests, transport checks, and screenshots |
| [Agent Skill](../skills/investigate-fix/SKILL.md) | Safe MCP investigation workflow |

## Original specifications

| Area | Documents |
|---|---|
| Product and scope | [Start here](00_START_HERE.md), [PRD](01_PRD.md), [implementation plan](08_IMPLEMENTATION_PLAN.md) |
| Security and data | [Threat model](02_THREAT_MODEL.md), [context assembly](03_DATA_AND_CHUNKING.md), [policy pipeline](04_SECURITY_PIPELINE.md), [attack tests](09_ATTACK_TESTS.md) |
| Architecture and interfaces | [Architecture](05_ARCHITECTURE.md), [API contract baseline](06_API_CONTRACT.md), [MCP and skills](13_MCP_AGENT_SKILLS.md) |
| Product design | [UI and UX](07_UI_UX_SPEC.md), [design system](12_DESIGN_SYSTEM.md) |
| Integrations | [AWS](14_AWS_INTEGRATION.md), [open-source contribution](15_OPEN_SOURCE_CONTRIBUTION.md) |
| Quality and operations | [Test strategy](16_TEST_STRATEGY.md), [deployment](17_DEPLOYMENT_AND_OPERATIONS.md), [audit](18_OBSERVABILITY_AND_AUDIT.md), [decisions](19_DECISIONS_AND_ASSUMPTIONS.md) |
| Demo and release | [Demo script](10_DEMO_SCRIPT.md), [judge checklist](11_JUDGE_CHECKLIST.md), [release and submission](20_RELEASE_AND_SUBMISSION.md) |

Relative links are intended for GitHub and local Markdown viewers. The original DOCX and PDF references remain in the user's supplied source folder; they are not duplicated into the source repository.
