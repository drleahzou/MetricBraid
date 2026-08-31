# Local files and pasted data quick start

Use this route if you have CSV, JSON, exported health records, screenshots, or
observations you can paste into a chat. It requires no Garmin or Oura login and
works with any agent that can read the MetricBraid framework.

## 1. Install

Choose the guide for your agent first:

- [Claude Code](2026-08-31-claude-code-quick-start.md): install the plugin.
- [Codex](2026-08-31-codex-quick-start.md): clone and open the repository.
- [Another agent](2026-08-31-other-agents-quick-start.md): clone and provide
  the operating instructions.

## 2. Activate or open MetricBraid

For Claude Code, run `/metricbraid:metricbraid-init` and select **pasted or
local exports only**. For Codex or another agent, open the cloned repository
and use that guide's setup prompt.

## 3. Configure your devices

List only the hardware that produced the observations. Include sensor
placement and any external heart-rate monitor when relevant. Leave a tiebreak
unset unless you intentionally prefer one source for reporting.

The supplied `devices.yaml` starts empty so no example hardware can be mistaken
for yours.

## 4. Provide the observations

Use whichever input is easiest:

- attach a CSV, JSON, screenshot, or provider export to the chat;
- paste a small structured observation directly;
- place private files under `data/` or `exports/` in the cloned repository;
- copy `food-log.example.csv` to the ignored `food-log.csv` for nutrition.

In the cloned MetricBraid repository, the supplied `.gitignore` excludes
`data/`, `exports/`, common export names, and `food-log.csv`. If you installed
the Claude plugin into another project, confirm that project's `.gitignore`
has equivalent rules before saving files there. Do not commit personal health
data.

Tell the agent which file belongs to which device and what date range it
covers. MetricBraid can route only the observations you actually provide; it
must say when a configured source is absent.

## 5. Verify

Ask:

> Verify my local-data MetricBraid setup. Read `devices.yaml`, identify each
> file or pasted observation I provided and its source, flag any configured
> device with no observations, and tell me whether I am ready to ask an
> analysis question. Do not analyse the measurements yet.

You are done when the agent correctly names your devices, files, sources, and
missing inputs. No restart or provider authentication is required unless you
later add a live integration.
