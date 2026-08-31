# MetricBraid for Codex

These instructions apply when a user asks Codex to set up MetricBraid or to
analyse wearable, health, activity, nutrition, or sensor observations with
MetricBraid. They do not require loading the health-routing framework for
ordinary repository maintenance.

## Setup requests

1. Read `docs/2026-08-31-codex-quick-start.md`, `SETUP.md`, and
   `devices.yaml` before changing anything.
2. Do not pull or analyse health data during setup.
3. Ask which devices and data sources the user actually uses. Never infer
   hardware from examples or from whichever server happens to respond.
4. Update `devices.yaml` with only their hardware, capability classes, sensor
   placement, external monitors, and optional tiebreak preferences.
5. Guide authentication only for selected providers. Never ask the user to
   paste passwords, client secrets, access tokens, refresh tokens, or MFA
   codes into chat.
6. Claude's `.mcp.json` is not Codex configuration. If the user wants live
   Garmin or Oura access, explain the proposed project-scoped Codex MCP change
   and get approval before creating or editing `.codex/config.toml`. Reuse the
   selected server definition from `.mcp.json`, forward secrets by environment
   variable name, and never write secret values into the repository.
7. End with the exact verification prompt from the Codex quick start and state
   whether setup is ready, pending a restart, or missing a specific step.

## Analysis requests

1. Read `devices.yaml` first.
2. Read `CLAUDE.md` as MetricBraid's canonical operating specification despite
   its platform-specific filename. Follow its routing, arbitration,
   deduplication, confidence, provenance, evidence, and reporting rules.
3. Read only the relevant material under `spec/` and `evidence/` for the
   question being answered.
4. If a configured source is unavailable, say so before analysing. Do not
   silently substitute another source or infer missing observations.
5. Never average competing sensors or hide an unresolved conflict.
