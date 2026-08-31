---
description: Set up MetricBraid sensor-evidence routing in the current project — installs the CLAUDE.md rules, the routed-observation spec, the device registry and the food-log template, and checks that the bundled MCP servers are connected.
---

Set up MetricBraid in the current project directory.

MetricBraid has three layers, and this command installs the first two. Keep
them distinct when explaining anything to the user:

- **Framework** — `CLAUDE.md` (routing rules) and `spec/` (the
  routed-observation contract). Hardware-agnostic; the user should not need
  to edit these.
- **User configuration** — `devices.yaml` and the MCP servers. Where hardware
  is named. **The only file most people ever edit.**
- **Evidence** — ships inside the skill as `references/`. Read-only here.

## Steps

1. **Check for an existing `CLAUDE.md`** in the project root.
   - If none exists, copy `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md` there.
   - If one exists, do **not** overwrite it. Show the user what the
     MetricBraid rules would add, and offer to append them under a
     `# Sensor evidence routing (MetricBraid)` heading, or to write the
     template to `CLAUDE.metricbraid.md` for them to merge by hand. Ask
     which they want before writing.

2. **Install the routed-observation spec.** Copy
   `${CLAUDE_PLUGIN_ROOT}/templates/spec/` to `spec/` in the project root if
   it isn't already there. This is the canonical form every routed metric
   takes — source, sensor, rule, routing basis, measurement confidence, what
   was merged, what must be disclosed — plus its JSON Schema and three worked
   examples. `CLAUDE.md` links to it, so skipping this leaves those links
   dangling.

3. **Install the device registry.** Copy
   `${CLAUDE_PLUGIN_ROOT}/templates/devices.yaml` into the project root if it
   isn't already there, then **ask the user what they actually wear** and fill
   it in — devices, capability classes, HR sensor placement, any external HR
   monitor, and tiebreak preferences. The shipped file is the author's setup
   (a ring plus a running watch) used as a worked example; it ships with
   commented presets for Whoop, Apple Watch, Fitbit, Polar, Coros, Suunto and
   Samsung.

   Be explicit with the user about two things:
   - Declaring a device grants **capabilities, not accuracy**. A device with
     no dossier still routes correctly but inherits only the device-agnostic
     baselines.
   - A **tiebreak is a preference, not evidence.** It decides which source
     gets reported when two devices declare the same capability class, and
     improves measurement confidence by nothing. Leaving one unset is a valid
     choice: the conflict is then reported as unresolved, with both values.

4. **Install the nutrition template.** Copy
   `${CLAUDE_PLUGIN_ROOT}/templates/food-log.example.csv` into the project
   root if it isn't already there. Tell the user to `cp` it to
   `food-log.csv` and add that filename to their `.gitignore` — it will
   contain personal data.

5. **Verify the bundled integrations.** The routing model is
   hardware-agnostic, but the shipped plumbing covers two providers. Check
   whether the `garmin` and `oura` MCP servers are connected in this session.
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
   - Other hardware works too: a community MCP server added to `.mcp.json`,
     or pasted exports. Declare it in `devices.yaml` and the rules apply
     unchanged.

6. **Confirm what was installed**, and state two things the user should
   expect to hear from the assistant afterwards:
   - **Rule A (passive signals) is provisional by design.** Its *routing* is
     reasoned from device design rather than measured, and the assistant is
     required to say so whenever an answer leans on it. That is separate from
     the measurements, which are graded individually — sleep duration is well
     validated even though the rule that routes it is not.
   - **Conflicts are not silently resolved.** When two devices disagree and
     no rule or tiebreak applies, the assistant reports both and says nothing
     resolved it. It will never average two sensors.

Do not pull or analyze any health data as part of this command. Setup only.
