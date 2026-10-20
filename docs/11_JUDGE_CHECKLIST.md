---
doc_id: "11"
title: "Judge and Track Compliance Checklist"
status: "draft"
owner: "Submission Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["13_MCP_AGENT_SKILLS.md", "14_AWS_INTEGRATION.md", "15_OPEN_SOURCE_CONTRIBUTION.md", "20_RELEASE_AND_SUBMISSION.md"]
---

# Judge and Track Compliance Checklist

## Primary track: Alexa+
- [ ] Working MCP integration uses a documented protocol/transport.
- [ ] Agent Skills are discoverable and useful for a defined workflow.
- [ ] Streamable HTTP transport is tested end-to-end.
- [ ] Web-based Alexa+ simulation is labelled accurately.
- [ ] Tool calls return structured, source-linked results.
- [ ] Demo can be reproduced from documented setup.
- [ ] No unsupported claim of official Alexa+ or device integration.

## Mini-challenge: AWS Builder
- [ ] One real AWS service/tool is integrated.
- [ ] README identifies service, purpose, and configuration.
- [ ] Credentials use least privilege and are not committed.
- [ ] Integration behavior and failure mode are tested.
- [ ] Evidence points to actual requests, outputs, logs, or artifacts.
- [ ] Cost and resource cleanup are considered.

## Mini-challenge: Open Source
- [ ] Public repository selected and contribution is relevant.
- [ ] Contribution was made during the eligible event window.
- [ ] Change respects project contribution guidelines and license.
- [ ] Tests or checks are recorded honestly.
- [ ] PR/commit/issue link is public and valid.
- [ ] Status is labelled draft/open/merged/rejected accurately.

## Product and security
- [ ] Approval is enforced server-side.
- [ ] Denial prevents the requested side effect.
- [ ] Untrusted content cannot override policy.
- [ ] Test output and state are tool-grounded.
- [ ] Secrets are redacted.
- [ ] Failure, timeout, and partial-success states are visible.

## Evidence index
For each checked item, add an evidence URL or artifact path, date verified, and owner. A checked box without evidence is not judge-ready.
