# Contributing

Read the root README for the supported workflow and setup. The original project specifications are indexed in `docs/README.md`; implementation status and external verification gates are tracked separately.

## Prepare a change

1. Create a branch for one focused change.
2. Keep credentials, `.env`, runtime databases, and private source context out of commits.
3. Preserve the server-side authorization boundary. Model output and external issue content must never authorize execution.
4. Update the relevant contract, documentation, and security tests when changing tools, approvals, integrations, or permissions.
5. Run `python -m pytest -q` and report actual failures or skipped checks. Use the optional browser and MCP client checks when their behavior changes.
6. Describe the problem, resulting behavior, validation, and remaining limitations in the pull request.

Do not label a configured adapter as a verified live integration. AWS evidence needs an actual successful request; GitHub publication needs a real artifact URL. The Alexa+ text interface remains a simulation unless a live integration is separately implemented and tested.

No project-wide license has been selected by the owner. Do not assume a license from third-party tools or from the hackathon's open-source contribution objective.
