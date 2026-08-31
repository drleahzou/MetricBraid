# Setup & Authentication Guide

**This is integration setup — the configuration layer, not the framework.**
The routing rules in `CLAUDE.md`, the contract in `spec/` and the dossiers in
`evidence/` need no setup and no credentials; they are hardware-agnostic. What
follows is specific to the two MCP servers this repo currently bundles. A
device reached some other way — a community MCP server, or a pasted export —
skips this file entirely and is declared in `devices.yaml` like any other.

The bundled MCP servers are configured in `.mcp.json` and install themselves
on first launch (Garmin via `uvx`, Oura via `npx`). The only thing they need
from you is credentials — one time each.

## Prerequisites

- `uv`/`uvx` (https://docs.astral.sh/uv/) — runs the Garmin server
  (it fetches Python 3.12 automatically)
- Node.js ≥ 18 with `npx` — runs the Oura server
- Python 3.9+ — for the Oura OAuth helper (stdlib only, nothing to install)

---

## 1. Oura Ring — OAuth2 (~10 minutes)

> **Read this first.** Oura **deprecated Personal Access Tokens in December
> 2025**. The PAT page at `cloud.ouraring.com/personal-access-tokens` still
> exists and will still happily hand you a token — but any PAT created after
> the deprecation returns **401 Unauthorized** on every request. This is the
> single most common way this setup fails. Tokens issued *before* the
> deprecation still work, but cannot be recreated once deleted, so if you
> have a working one, **do not delete it**.
>
> **OAuth2 is the only path that works for a new setup.**

### 1a. Register an application

1. Go to https://cloud.ouraring.com/applications and create a new
   application.
2. Set the redirect URI to **exactly**:
   ```
   http://localhost:8080/callback
   ```
   A trailing slash or a different port will cause a redirect-URI mismatch.
3. Copy the **Client ID** and **Client Secret**.

### 1b. Authorize

Export the credentials, then run the login flow once:

```bash
export OURA_CLIENT_ID="your-client-id"
export OURA_CLIENT_SECRET="your-client-secret"
python3 scripts/oura_auth.py login
```

Your browser opens Oura's consent screen. Approve it, and the helper
exchanges the code and saves tokens to `~/.oura-mcp/tokens.json` (mode
`0600`, outside the repo).

### 1c. Make the token available to the MCP server

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

## 2. Garmin Connect (5 minutes)

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

## 3. Nutrition (optional — Rule D)

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

## 4. Verify both connections

Start a new Claude Code session in this project and ask:

> Pull yesterday's sleep from Oura and yesterday's stats from Garmin.

Both should return real data.

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Oura tools return **401** | Token is a post-Dec-2025 PAT (dead), or an expired OAuth token | Re-run `oura_auth.py token`; if it's a PAT, migrate to OAuth2 (§1) |
| Oura 401 right after it worked | Access token expired (~24h) | `export OURA_ACCESS_TOKEN="$(python3 scripts/oura_auth.py token)"`, restart the session |
| `invalid_grant` on refresh | Single-use refresh token was already redeemed | Re-run `python3 scripts/oura_auth.py login` |
| Redirect URI mismatch | App's URI ≠ `http://localhost:8080/callback` | Fix it in the Oura app settings — must match exactly |
| Garmin server exits at startup | No cached tokens | Re-run `garmin-mcp-auth` (§2) |
| Env var set but server can't see it | MCP servers capture their environment at **session start** | Restart the Claude Code session (full quit if launched from a GUI) |

## Security

- `.gitignore` blocks `.env*` files, token directories, and
  `.claude/settings.local.json` — never commit credentials.
- Oura tokens live in `~/.oura-mcp/`, Garmin's in `~/.garminconnect/` —
  both outside this repo.
- The Oura token grants read access to all your Oura data. Revoke it any
  time from https://cloud.ouraring.com/applications.
