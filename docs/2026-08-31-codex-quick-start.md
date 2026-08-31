# Codex quick start

Use this route for the ChatGPT desktop app's Codex workspace or Codex CLI. The
repository includes `AGENTS.md`, so Codex automatically learns how to set up
and apply MetricBraid whenever you open this folder.

## 1. Install

Clone the repository into a folder you can keep private:

```bash
git clone https://github.com/drleahzou/MetricBraid.git
cd MetricBraid
```

The repository contains no personal health data. Your own exports and local
credentials are ignored by its supplied `.gitignore`.

## 2. Open in Codex

Open the cloned `MetricBraid` folder as a project in the ChatGPT desktop app,
or start Codex CLI from that folder:

```bash
codex
```

Codex reads the repository's `AGENTS.md` at the start of each new session.

## 3. Configure your devices

Send:

> Set up MetricBraid in this project. Do not analyse health data yet. Ask me
> which devices and data sources I use, then update `devices.yaml` with only
> my actual hardware and explain any remaining setup step.

The safe template starts with no active devices or tiebreak preferences.

## 4. Connect data or provide files

Choose the simplest route that matches your needs:

- **Exports or pasted observations:** no connection is required. Follow the
  [local-data quick start](2026-08-31-local-data-quick-start.md).
- **Oura or Garmin:** complete the relevant authentication section in
  [`SETUP.md`](../SETUP.md), then ask Codex:

  > Connect my selected MetricBraid data sources in this project. Reuse the
  > server definitions in `.mcp.json`, translate only those selected sources
  > into project-scoped Codex MCP configuration, keep all secrets in
  > environment variables, and show me the proposed configuration before
  > writing it.

Claude's `.mcp.json` is not loaded automatically by Codex. Codex will explain
the required `.codex/config.toml` change and ask before writing it. Restart the
Codex session after authentication or MCP configuration changes.

## 5. Verify

Ask this in the fresh session, removing any provider you did not configure:

> Verify my MetricBraid setup. Pull yesterday's sleep from Oura and
> yesterday's stats from Garmin, then report each connection as ready or
> explain the exact remaining setup step. Do not combine or analyse the
> measurements yet.

For local-only data, ask:

> Verify my MetricBraid setup without using a live integration. Confirm that
> `devices.yaml` describes only my hardware, identify the local file I will
> provide, and tell me whether I am ready to ask an analysis question.

You are done when the selected live sources return real data, or when Codex
confirms the local file and device registry are ready.

Codex behavior described here follows the official OpenAI documentation for
[`AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and
[MCP configuration](https://learn.chatgpt.com/docs/extend/mcp).
