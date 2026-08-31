---
description: Set up MetricBraid in this project, including device configuration, prerequisites, authentication guidance, and a final connection check.
---

Set up MetricBraid in the current project directory. This is an interactive
setup command. Do not pull or analyze any health data while running it.

MetricBraid has three layers. Keep them distinct when explaining the setup:

- **Framework** — `CLAUDE.md` contains hardware-agnostic routing rules. The
  user should not need to edit it.
- **User configuration** — `devices.yaml`, credentials, and MCP servers name
  the user's hardware and integrations. This is the layer being configured.
- **Evidence** — read-only dossiers and the routed-observation contract ship
  inside the plugin skill's `references/` directory.

Use the phases below in order. Report setup states as **ready**, **pending a
restart**, **not configured**, or **not selected**. A provider that has not
been authenticated on a first run is expected setup work, not a failed
installation.

## Phase 1 — Welcome and preflight

1. Tell the user what will happen: setup installs project files, asks about
   their devices, guides authentication for selected providers, and ends with
   a verification prompt. It does not read any health data.
2. Ask which data sources they intend to use now:
   - Oura;
   - Garmin;
   - another integration;
   - pasted or local exports only.
   Do not require Oura or Garmin just because their MCP servers are bundled.
3. Check prerequisites only for the selected bundled providers:
   - Oura: Node.js 18 or newer with `npx`, plus Python 3.9 or newer for the
     dependency-free OAuth helper.
   - Garmin: `uvx`; it fetches the required Python runtime itself.
4. State every prerequisite result plainly. If one is missing, point to the
   relevant section of `${CLAUDE_PLUGIN_ROOT}/SETUP.md`. Do not install or
   upgrade system software without the user's explicit approval. Continue
   setting up unaffected providers and project files.
5. Check whether each selected provider is already connected in this session.
   Treat a missing first-run credential as **not configured**. Remember that
   MCP servers capture their environment at session start, so credentials
   added during this command cannot make the current server reconnect. The
   plugin's static MCP configuration may also attempt to start a bundled
   provider the user does not use; label it **not selected** and explain that
   its disconnected state does not make the installation fail.

## Phase 2 — Install the project files

Never overwrite an existing file silently.

1. **Routing rules:**
   - If the project has no `CLAUDE.md`, copy
     `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md` there.
   - If one exists, show what MetricBraid would add and ask whether to append
     it under `# Sensor evidence routing (MetricBraid)` or write
     `CLAUDE.metricbraid.md` for manual merging.
2. **Device registry:** copy
   `${CLAUDE_PLUGIN_ROOT}/templates/devices.yaml` to `devices.yaml` only when
   the project does not already have one. The safe template declares no
   active devices.
3. Ask what the user actually wears and update `devices.yaml` with:
   - devices and stable IDs;
   - capability classes;
   - heart-rate sensor placement;
   - external heart-rate monitors and when they are worn;
   - optional tiebreak preferences.

   Explain that declaring a capability does not claim accuracy. A tiebreak is
   a reporting preference, not evidence, and leaving it unset is valid: both
   conflicting values will then be reported as unresolved.
4. **Self-contained setup support:**
   - Copy `${CLAUDE_PLUGIN_ROOT}/SETUP.md` to `SETUP.md` if it is absent.
   - Ensure a `scripts/` directory exists, then copy
     `${CLAUDE_PLUGIN_ROOT}/scripts/oura_auth.py` to
     `scripts/oura_auth.py` if it is absent.
   - If either destination already exists, leave it unchanged and say so.
5. **Nutrition template:** copy
   `${CLAUDE_PLUGIN_ROOT}/templates/food-log.example.csv` to the project root
   if it is absent. If the user wants nutrition routing, tell them to copy it
   to `food-log.csv`; that filename is personal data and should be gitignored.

## Phase 3 — Authenticate selected providers

Guide only the providers selected in Phase 1. Never ask the user to paste a
password, client secret, access token, refresh token, or MFA code into chat.
Have them enter secrets directly in their terminal or provider page.

### Oura

Use the project-local `SETUP.md` and `scripts/oura_auth.py` installed above.
New setups must use OAuth2. Oura deprecated Personal Access Tokens in December
2025; newly created PATs return 401 even though the PAT page may still issue
them. Never advise deleting a working pre-deprecation PAT as a first step,
because it cannot be recreated.

The user must register an Oura application, set the documented redirect URI,
export `OURA_CLIENT_ID` and `OURA_CLIENT_SECRET` in their terminal, and run:

```bash
python3 scripts/oura_auth.py login
```

They should configure `OURA_ACCESS_TOKEN` using the helper as shown in
`SETUP.md`, rather than pasting a short-lived literal token into a profile.

### Garmin

Have the user run the interactive `garmin-mcp-auth` command shown in
`SETUP.md`. It is the recommended route and supports MFA. Credentials and MFA
codes stay in the terminal prompt; they must not be entered into chat.

### Other integrations or local exports

No bundled authentication applies. Confirm how the observations will enter
the project, declare the hardware in `devices.yaml`, and explain that the same
routing rules apply.

## Phase 4 — Readiness and exact next action

1. Summarize every installed, preserved, or skipped file.
2. Give one status for each selected provider:
   - **ready** if it was already connected and its prerequisites are present;
   - **pending a restart** if credentials were added or changed;
   - **not configured** if a required auth step remains;
   - **not selected** for bundled providers the user does not use.
3. Do not call an integration broken merely because it cannot reconnect in the
   current session after first-run authentication.
4. If any credential or environment value changed, tell the user to exit and
   start a fresh Claude Code session in this project. A plugin reload alone is
   not enough for MCP environment changes.
5. End with this explicit verification prompt for the selected providers,
   removing any provider the user did not select:

   > Verify my MetricBraid setup. Pull yesterday's sleep from Oura and
   > yesterday's stats from Garmin, then report each connection as ready or
   > explain the exact remaining setup step. Do not combine or analyze the
   > measurements yet.

6. Define the finish line: setup is complete when the fresh session returns
   real data from each selected provider and `devices.yaml` contains only the
   user's actual hardware. If the user selected only local or pasted data,
   setup is complete when the files are installed and the registry is correct.

Also tell the user what normal MetricBraid answers will do after setup:

- Rule A passive routing is provisional by design and will be labelled as
  such separately from each measurement's confidence.
- Unresolved conflicts remain visible with both values; MetricBraid never
  silently averages two sensors.
