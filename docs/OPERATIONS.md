# Operations and integration guide

Run the commands below from the repository root. This guide covers detailed setup, integration boundaries, execution limits, and local operations.

## Run locally

Requires Python 3.12. The included demonstration needs no account, model key, Docker, or network access after dependencies are installed.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock
.\.venv\Scripts\python.exe -m sde_agent
```

On macOS/Linux, use `.venv/bin/python` instead. Dependencies are pinned; the lock includes the Windows-only package marker. Startup binds to `127.0.0.1:8000` and prints a private login link. Open it in your browser. Keep it private: its fragment contains the single local operator token. The browser stores that token in session storage and removes it from the address bar. The service has no shared-hosting or multi-user claim.

Choose **Try the included demo → Build a plan → Approve action**. Review the baseline failure and the three actual passing regression tests after the patch. Start a second run and choose **Deny** to show that execution stops. **Plan only** never creates an execution approval or workspace.

The fixture issue and deterministic plan are explicitly labelled synthetic. Its Python subprocess runs only the shipped, exact fixture and patch. Any external repository code requires the Docker executor. No untrusted code runs through a host-shell fallback.

## Connect GitHub and Amazon Bedrock

Copy `.env.example` to `.env` and configure the exact repository allowlist, GitHub fine-grained token, region, and a Bedrock model you can access. Use the AWS SDK credential chain or your local AWS profile; do not add credentials to source. Restart after configuration changes.

1. Create an investigation with a matching `https://github.com/owner/repo/issues/number` URL. Source and CI are read at a pinned commit from the repository's default branch.
2. Inspect collected files. Approve the exact Bedrock request before code is sent to AWS or inference is billed. Output is bounded to 4,096 tokens and one request per approval, with no automatic provider retry. The app does not estimate prices; set an account budget before enabling this path.
3. Inspect the model-generated plan, acceptance criteria, and complete proposed diff. push thisModel output cannot choose commands or grant permissions.
4. Install Docker Desktop/Engine and pre-pull the sandbox image: `docker pull python:3.12-slim`. For a shared or sensitive environment configure an audited image digest in `SDE_SANDBOX_IMAGE`. The executor never pulls an image implicitly.
5. Approve the patch/test action. The exact patch is applied to an ephemeral copy and the fixed unittest command runs before and after, without network, credentials, root privileges, or host Docker socket inside the container. Limits: 256 MB, one CPU, 32 PIDs, 45 seconds per check, 1 MB output kill threshold, 64 KB retained per stream. Counts come from actual unittest output; no tests means no successful verification.
6. After tests pass, enable `SDE_GITHUB_WRITE=true` only if the configured token has the required rights. **Review draft PR action** displays the exact branch, base commit, title, body, and tested patch. A separate approval creates Git objects, a new branch, and a draft PR. The app never merges.

Current live scope: small Python standard-library projects with unittest discovery, at most 40 non-hidden `.py` files and 300 KB retrieved source. Dependency installation, arbitrary build commands, other languages, cloning entire repositories, test-file modification, and automatic issue selection are not implemented. Repositories that need additional files or packages will not verify with this executor. The dashboard displays failures honestly.

GitHub permissions: Metadata read; Issues read; Checks read; Contents read. To publish, add Contents write and Pull requests write for only the disposable target. Bedrock IAM needs `bedrock:InvokeModel` on the selected model/inference profile and any required underlying model resources. See `infra/bedrock-policy.example.json` and adapt exact ARNs to your account. No cloud resources are provisioned by this project.

## MCP and Agent Skill

Endpoint: `http://127.0.0.1:8000/mcp/` using Streamable HTTP. Authenticate using `Authorization: Bearer <operator token>`. Use `Accept: application/json, text/event-stream`. MCP SDK 1.30.0 handles initialization, protocol negotiation, schema validation, notifications, and errors. Transport is stateless with JSON responses; reconnect by initializing a fresh client. It does not offer SSE replay or durable transport sessions.

The seven tools are `get_issue`, `search_repository`, `read_file`, `get_ci_status`, `propose_change`, `run_tests`, and `create_draft_pull_request`. Run-oriented tools require a dashboard-created run ID. Read tools only access bounded retrieved context. `propose_change` exposes the plan; `run_tests` returns actual execution evidence; neither bypasses visual approval. Draft PR requests create approvals rather than publishing immediately. Unsupported notification and generic AWS-status tools are not advertised.

The reusable skill is `skills/investigate-fix/SKILL.md`. Install that directory into your coding agent's skill directory and configure the MCP endpoint using your client's remote-HTTP configuration. A usable skill artifact is included; execution inside a separate agent ecosystem has not been verified.

```powershell
$env:SDE_API_TOKEN = "your-running-service-token"
python scripts/verify_mcp.py
```

This script uses the official MCP client SDK to initialize twice, discover tools, retrieve a synthetic issue and source provenance, reject a path escape, and reconnect. It prints real results without printing the token. Use `SDE_BASE_URL` for a non-default local port.

## API, tests, and operations

All `/api/*`, `/mcp/*`, and OpenAPI documentation routes require the token. `/health` is a minimal public liveness check; `/api/ready` checks database availability and audit-chain integrity. OpenAPI at `/openapi.json` is the authoritative typed HTTP contract. API responses use `{request_id,status,data,error}`; MCP uses protocol-native envelopes. Unknown JSON fields are rejected.

```powershell
python -m pytest -q
```

See `evidence/` for captured verification reports and screenshots. Tests cover actual fixture execution plus authorization and abuse scenarios; they do not imply live account, Docker-isolation, or hackathon eligibility verification. The hosted [Verify workflow run](https://github.com/udbhav-metla/sde-agent-starter-kit/actions/runs/39458367247) passed for the initially published implementation.

The current build passed **32 automated tests**, the official MCP SDK client check including reconnect, and the browser workflow at 1440×1000 and 390×844. A wheel build also passed. `BUILD_MANIFEST.json` records source hashes and external gates; this source snapshot is not pinned to an upstream Git commit.

For the optional browser check, run the server separately, install the development browser dependency with `npm install` and `npx playwright install chromium`, set `SDE_API_TOKEN` and optional `SDE_BASE_URL`, then run `npm run test:browser`. It exercises the demo and writes screenshots under `evidence/`. `SDE_BROWSER_PATH` optionally selects a local Chrome/Edge executable. This package.json is only for browser checks; the application itself needs no Node runtime.

Records use SQLite WAL under `.data/`, with append-only event triggers and a SHA-256 audit chain. The chain detects edits when the database remains under application control; a host administrator can rewrite the entire database, so this is not an externally anchored tamper-proof log. Source context and evidence are redacted before persistence, model requests, and display; heuristic filtering cannot guarantee detection of every unknown secret. Use disposable, non-sensitive repositories for the demo.

The server caps concurrent active operations at two, limits authenticated requests to 360/minute, rejects bodies over 128 KB, denies foreign hosts/origins, and never exposes arbitrary shell commands. Approval decisions are consumed under a process lock. Run only one service process against a data directory. Remote writes are never automatically retried; after an interrupted or failed publication, the run is marked partial and must be reconciled against GitHub. Git objects or a branch may exist if PR creation failed.

Stop with Ctrl+C. To reset, stop the service, preserve any needed evidence, and remove only this project's `.data` directory (or the exact configured `SDE_DATA_DIR`). Local records are retained until that explicit reset; there is no automatic expiry/deletion scheduler. For demos, reset immediately after exporting required non-sensitive evidence. On restart, interrupted active runs become partial rather than silently resuming. Revoke leaked tokens and rotate the local operator token before restarting.

## Remaining submission gates

The application includes GitHub and Bedrock adapters, but real AWS and draft-PR calls require your configured account and repository and have not been verified in this build session. Docker was not installed in the build environment. Alexa+ is a clearly labelled text simulation. No open-source contribution was published, and event eligibility has not been confirmed. These gates remain visible rather than being represented as completed features.

Implementation references: [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk), [Bedrock Converse](https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-runtime/client/converse.html), [GitHub Git trees](https://docs.github.com/en/rest/git/trees), and [GitHub draft pull requests](https://docs.github.com/en/rest/pulls/pulls#create-a-pull-request).
