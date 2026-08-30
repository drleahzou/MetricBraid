---
description: Set up MetricBraid health-data routing in the current project — installs the CLAUDE.md rules, the food-log template, and checks that the Garmin and Oura MCP servers are connected.
---

Set up MetricBraid in the current project directory.

## Steps

1. **Check for an existing `CLAUDE.md`** in the project root.
   - If none exists, copy `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md` there.
   - If one exists, do **not** overwrite it. Show the user what the
     MetricBraid rules would add, and offer to append them under a
     `# Health data routing (MetricBraid)` heading, or to write the
     template to `CLAUDE.metricbraid.md` for them to merge by hand. Ask
     which they want before writing.

2. **Install the device registry.** Copy
   `${CLAUDE_PLUGIN_ROOT}/templates/devices.yaml` into the project root if it
   isn't already there, then **ask the user what they actually wear** and fill
   it in — devices, capability classes, HR sensor placement, and any external
   HR monitor. The shipped file is the author's setup (a ring plus a running
   watch) used as a worked example; it ships with commented presets for Whoop,
   Apple Watch, Fitbit, Polar, Coros, Suunto and Samsung.

   Be explicit with the user that declaring a device grants **capabilities,
   not accuracy** — a device with no dossier in `evidence/devices/` still
   routes correctly but inherits only the device-agnostic baselines.

3. **Install the nutrition template.** Copy
   `${CLAUDE_PLUGIN_ROOT}/templates/food-log.example.csv` into the project
   root if it isn't already there. Tell the user to `cp` it to
   `food-log.csv` and add that filename to their `.gitignore` — it will
   contain personal data.

4. **Verify the MCP servers.** Check whether the `garmin` and `oura` MCP
   servers are connected in this session.
   - Report the status of each plainly. Do not assume they work.
   - If **Oura** is failing with a 401: the most likely cause is a Personal
     Access Token. Oura deprecated PATs in December 2025 and newly created
     ones return 401 — the PAT page still issues them, which is why this
     traps people. Point the user to `scripts/oura_auth.py` in the
     MetricBraid repo for the OAuth2 flow. **Never advise regenerating or
     deleting an existing token as a first move** — a pre-deprecation PAT
     that still works cannot be replaced once deleted.
   - If **Garmin** exited at startup, that is almost always missing
     authentication — have them run `garmin-mcp-auth`.
   - Remember MCP servers capture their environment at session start, so a
     session restart is required after any env change.

5. **Confirm what was installed** and note that Rule A (passive signals) is
   marked PROVISIONAL by design — the assistant is required to say so
   whenever an answer leans on it.

Do not pull or analyze any health data as part of this command. Setup only.
