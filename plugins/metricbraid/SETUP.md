# Setup & Authentication Guide

**This is integration setup — the configuration layer, not the framework.**
The routing rules in `CLAUDE.md`, the contract in `spec/` and the dossiers in
`evidence/` need no setup and no credentials; they are hardware-agnostic. What
follows is specific to the two MCP servers this repo currently bundles. A
device reached some other way — a community MCP server, or a pasted export —
skips this file entirely and is declared in `devices.yaml` like any other.

The bundled MCP server definitions live in `.mcp.json`. Claude Code reads that
format directly; Codex and other agents may use a different configuration
format and treat it as a reference. The servers install themselves when
launched (Garmin via `uvx`, Oura via `npx`). The only thing they need from you
is credentials — one time each.

## Use this after choosing your platform

Start with the environment-specific quick start. In the cloned repository,
choose it near the top of `README.md`. If Claude init copied this file into
another project, you are already following the Claude Code route. This file is
the shared reference for device configuration, provider authentication,
security and troubleshooting; do not complete a provider section unless you
use that provider.

**Claude Code plugin:** after installing the plugin, run `/reload-plugins`,
then run `/metricbraid:metricbraid-init` in the project where you want to use
MetricBraid. The command checks prerequisites, installs this guide and the
OAuth helper into your project, asks about your actual devices, and walks you
through the relevant authentication steps.

**Codex or another agent:** follow its quick start to clone and open the
repository, then configure `devices.yaml` before asking health questions. The
safe default declares no hardware, so MetricBraid cannot route against someone
else's device setup by accident. Claude's `.mcp.json` does not automatically
configure another agent.

Only set up providers you actually use. Garmin and Oura are bundled, but
neither is required; community integrations and pasted exports work with the
same routing rules. Because the bundled MCP configuration is static, Claude
Code may still attempt to start an unused provider. Its disconnected state is
expected and does not block setup; init reports it as **not selected**.

## 1. Configure your devices (required)

Open `devices.yaml` and replace the empty `devices: []` list with only the
hardware you actually wear. Commented examples cover Oura, Garmin, Whoop,
Apple Watch, Fitbit, Polar, Coros, Suunto, Samsung and Withings.

For each device, declare its capability classes and heart-rate sensor
placement. Also declare any external HR monitor and the activities for which
you wear it. Tiebreaks are optional: they are reporting preferences, not
evidence, and leaving one `null` correctly preserves both values as an
unresolved conflict.

Declaring a capability never claims the device is accurate. Devices without a
dossier still route by capability but inherit only device-agnostic measurement
guidance.

## Prerequisites for selected providers

- `uv`/`uvx` (https://docs.astral.sh/uv/) — required only for Garmin; it runs the server
  (it fetches Python 3.12 automatically)
- Node.js ≥ 18 with `npx` — required only for Oura; it runs the server
- Python 3.9+ — required only for Oura's OAuth helper (stdlib only, nothing to install)

---

## 2. Oura Ring — OAuth2 (~10 minutes)

> **Read this first.** Oura **deprecated Personal Access Tokens in December
> 2025**. The PAT page at `cloud.ouraring.com/personal-access-tokens` still
> exists and will still happily hand you a token — but any PAT created after
> the deprecation returns **401 Unauthorized** on every request. This is the
> single most common way this setup fails. Tokens issued *before* the
> deprecation still work, but cannot be recreated once deleted, so if you
> have a working one, **do not delete it**.
>
> **OAuth2 is the only path that works for a new setup.**

### 2a. Register an application

1. Go to https://cloud.ouraring.com/applications and create a new
   application.
2. Set the redirect URI to **exactly**:
   ```
   http://localhost:8080/callback
   ```
   A trailing slash or a different port will cause a redirect-URI mismatch.
3. Copy the **Client ID** and **Client Secret**.

### 2b. Authorize

Export the credentials, then run the login flow once:

```bash
export OURA_CLIENT_ID="your-client-id"
export OURA_CLIENT_SECRET="your-client-secret"
python3 scripts/oura_auth.py login
```

Your browser opens Oura's consent screen. Approve it, and the helper
exchanges the code and saves tokens to `~/.oura-mcp/tokens.json` (mode
`0600`, outside the repo).

### 2c. Make the token available to the MCP server

Oura access tokens **expire in about 24 hours**, so don't paste a literal
token into your profile — call the helper, which refreshes automatically:

```bash
export OURA_ACCESS_TOKEN="$(python3 /full/path/to/scripts/oura_auth.py token)"
```

Put those three `export` lines (`OURA_CLIENT_ID`, `OURA_CLIENT_SECRET`,
`OURA_ACCESS_TOKEN`) in your shell profile. `.mcp.json` picks the token up
via `${OURA_ACCESS_TOKEN}`.

> **Note on refresh tokens:** Oura refresh tokens are **single-use** — they
> are invalidated the moment they're redeemed, and the response contains a
> replacement. `oura_auth.py` persists the new one on every refresh. A
> hand-rolled script that forgets this step works exactly once and then
> fails, which is a confusing failure to debug.

**Claude Code on the web / remote sessions:** browser-based OAuth and a
local token cache don't survive an ephemeral container. Run the flow
locally and use Oura from local sessions, or add a long-lived
`OURA_ACCESS_TOKEN` in the project's environment settings and refresh it
manually when it expires.

---

## 3. Garmin Connect (5 minutes)

Garmin has no personal-token API for consumers — the server logs in with
your Garmin Connect email/password once, completes Garmin's OAuth token
exchange, and stores refresh tokens in `~/.garminconnect/` (valid ~6
months, refreshed automatically).

**Option A — interactive auth (recommended; required if you have MFA):**

```bash
uvx --python 3.12 --from git+https://github.com/Taxuspt/garmin_mcp garmin-mcp-auth
```

Enter your Garmin email, password, and MFA code when prompted. Tokens are
saved to `~/.garminconnect/`. You never need to store your password.

**Option B — environment variables (only works without MFA):**

Set `GARMIN_EMAIL` and `GARMIN_PASSWORD` in your shell profile. The server
logs in on startup and caches tokens to `~/.garminconnect/`.

**Remote/ephemeral sessions note:** remote containers are wiped between
sessions, so `~/.garminconnect/` doesn't persist there. For remote use,
either use Option B env vars (no-MFA accounts), or run Option A locally and
use Garmin from local sessions.

**Token expiry:** after ~6 months, re-run
`garmin-mcp-auth --force-reauth`.

---

## 4. Nutrition (optional — Rule D)

There is no MCP server for food logging, so nutrition data only ever
arrives by hand. Copy the template and fill it in from whatever logger you
use:

```bash
cp food-log.example.csv food-log.csv
```

`food-log.csv` is gitignored. See the **NUTRITION DATA INTAKE** section of
`CLAUDE.md` for how the assistant is instructed to weight these entries.

Rule D is also the worked proof that the framework does not need a server:
intake is routed, graded and reported with provenance like anything else, and
has never had an integration behind it.

---

## 5. Restart and verify selected connections

MCP servers capture credentials and environment values when the session
starts. After adding or changing credentials, fully exit and start a new
Claude Code session in this project. Then ask, removing any provider you did
not configure:

> Verify my MetricBraid setup. Pull yesterday's sleep from Oura and
> yesterday's stats from Garmin, then report each connection as ready or
> explain the exact remaining setup step. Do not combine or analyze the
> measurements yet.

You are done when every selected provider returns real data and
`devices.yaml` lists only your actual hardware. If you use only pasted or
local files, you are done when the project files are installed and the device
registry is correct.

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Oura tools return **401** | Token is a post-Dec-2025 PAT (dead), or an expired OAuth token | Re-run `oura_auth.py token`; if it's a PAT, migrate to OAuth2 (§2) |
| Oura 401 right after it worked | Access token expired (~24h) | `export OURA_ACCESS_TOKEN="$(python3 scripts/oura_auth.py token)"`, restart the session |
| `invalid_grant` on refresh | Single-use refresh token was already redeemed | Re-run `python3 scripts/oura_auth.py login` |
| Redirect URI mismatch | App's URI ≠ `http://localhost:8080/callback` | Fix it in the Oura app settings — must match exactly |
| Garmin server exits at startup | No cached tokens | Re-run `garmin-mcp-auth` (§3) |
| Env var set but server can't see it | MCP servers capture their environment at **session start** | Restart the Claude Code session (full quit if launched from a GUI) |

## Security

- This template repository's `.gitignore` blocks `.env*` files, token
  directories, and `.claude/settings.local.json`. If init copied this guide
  into another project, confirm that project's ignore rules offer the same
  protection. Never commit credentials.
- Oura tokens live in `~/.oura-mcp/`, Garmin's in `~/.garminconnect/` —
  both outside this repo.
- The Oura token grants read access to all your Oura data. Revoke it any
  time from https://cloud.ouraring.com/applications.
