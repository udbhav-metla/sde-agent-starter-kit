# Verification evidence

These artifacts were captured during local verification on 20 October 2026. They do not demonstrate live AWS access, a published GitHub draft PR, Docker isolation, a hosted CI run, or a completed upstream contribution.

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
