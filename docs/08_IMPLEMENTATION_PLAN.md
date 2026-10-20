---
doc_id: "08"
title: "Implementation Plan"
status: "baseline"
owner: "Project Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["01_PRD.md", "02_THREAT_MODEL.md", "05_ARCHITECTURE.md", "06_API_CONTRACT.md", "07_UI_UX_SPEC.md"]
---

# Implementation Plan

## Guiding rule
Build one vertical slice end-to-end before adding integrations. A polished dashboard without a real tool call is not a working agent.

## Phase 0 — Resolve decisions
- Select repository provider, model provider, stack, sandbox, AWS service, and open-source target.
- Confirm event rules, deadlines, evidence format, and Alexa+ track acceptance.
- Freeze initial tool schemas and threat boundaries.

**Exit:** decisions recorded; scope is small enough for a repeatable demo.

## Phase 1 — Skeleton
- Create repository, environment template, linting, tests, and local startup.
- Build app shell, navigation, run states, and empty/error/loading states.
- Add backend health and configuration validation.

**Exit:** clean clone starts using documented commands.

## Phase 2 — MCP vertical slice
- Implement one read-only MCP tool over Streamable HTTP.
- Add Agent Skill instructions for the issue-investigation workflow.
- Connect the UI to create a run and display actual events.

**Exit:** a real source can be read and shown with provenance.

## Phase 3 — Plan and policy
- Assemble source-linked context and generate a structured plan.
- Add action classification and approval persistence.
- Test denied, expired, and changed-parameter approvals.

**Exit:** no protected action executes without valid authorization.

## Phase 4 — Sandboxed change and verification
- Create a local patch in an isolated workspace.
- Run a small allowlisted test command.
- Display actual diff, stdout/stderr, exit code, and test result.

**Exit:** a repeatable issue-to-test flow works with real output.

## Phase 5 — Delivery and integrations
- Add draft PR creation behind explicit approval.
- Add one real AWS service integration with documented scope and evidence.
- Complete one meaningful open-source contribution.

**Exit:** external artifacts can be independently inspected.

## Phase 6 — Hardening and demo
- Run attack tests, accessibility checks, and fault injection.
- Rehearse the demo from a clean environment.
- Freeze a known-good build and capture evidence.

**Exit:** judge checklist passes and every claim has a source.

## Prioritization
Must-have: MCP transport, one useful skill, one real tool, policy gate, evidence timeline, test result, repeatable demo. Should-have: draft PR, AWS integration, open-source contribution proof. Defer broad multi-agent orchestration, multiple model providers, complex analytics, and full autonomous deployment.
