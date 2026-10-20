# Verification evidence

These artifacts were captured during local verification on 20 October 2026. They do not demonstrate live AWS access, a published GitHub draft PR, Docker isolation, a hosted CI run, or a completed upstream contribution.

After publication, the [hosted GitHub Actions workflow](https://github.com/udbhav-metla/sde-agent-starter-kit/actions/runs/39458367247) completed successfully for commit `b52dd53ecf9456cc5a5cc78698b5937ecfc90a96`. Its separate result is recorded in [github-actions.json](github-actions.json).

| Artifact | What it records |
|---|---|
| [tests.txt](tests.txt) | 32 automated tests passed, with one dependency deprecation warning |
| [tests.xml](tests.xml) | Machine-readable pytest JUnit report |
| [mcp-client.json](mcp-client.json) | Official MCP SDK initialization, discovery, provenance search, path rejection, and reconnect |
| [browser-check.json](browser-check.json) | Browser workflow and mobile overflow check |
| [overview.png](overview.png) | Desktop overview |
| [approval.png](approval.png) | Exact-action approval and proposed diff |
| [verification.png](verification.png) | Actual before/after regression-test output |
| [mobile.png](mobile.png) | Mobile overview |

The included issue and plan are synthetic and labelled accordingly. The fixture's tests were actually executed. See the root README for commands to reproduce the automated and optional integration checks. Keep any future evidence redacted; never commit credentials, private repository context, or live runtime databases.
