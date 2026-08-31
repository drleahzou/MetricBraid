# Other AI agents quick start

Use this route for Gemini CLI, Cursor, another MCP-capable agent, or a custom
agent. MetricBraid's reasoning framework is portable, but these environments
do not yet have a packaged MetricBraid installer. Local files are the simplest
and most predictable data path.

## 1. Install

Clone the repository:

```bash
git clone https://github.com/drleahzou/MetricBraid.git
cd MetricBraid
```

## 2. Open the repository

Open the cloned folder in your agent. If the agent supports persistent project
instructions, point it to `CLAUDE.md` as the canonical MetricBraid operating
specification. The filename is platform-specific; the routing model is not.

## 3. Configure your devices

Give the agent this setup prompt:

> Set up MetricBraid in this project without analysing health data. Read
> `CLAUDE.md`, `devices.yaml`, and `SETUP.md`. Ask which devices and data
> sources I actually use, then update `devices.yaml` with only my hardware.
> Do not infer devices from examples or available integrations.

If your agent does not retain project instructions, include this shorter
instruction at the start of future health-data sessions:

> Apply the MetricBraid rules in `CLAUDE.md` before analysing these sensor
> observations. Read `devices.yaml` first and keep provenance and unresolved
> conflicts visible.

## 4. Connect data or provide files

For the lowest-friction route, use the
[local-data quick start](2026-08-31-local-data-quick-start.md).

For a live integration, your agent must support local MCP servers or another
compatible connector. Use the Garmin and Oura server definitions in
`.mcp.json` as a reference, follow the authentication steps in
[`SETUP.md`](../SETUP.md), and consult that agent's documentation for its
configuration format. Do not paste secrets into agent instructions or commit
them to the repository.

## 5. Verify

For local data, ask:

> Confirm that you have read the MetricBraid operating rules and
> `devices.yaml`. Identify the observation file I provided, state which device
> records you expect it to contain, and tell me whether setup is ready. Do not
> analyse the measurements yet.

For a live source, first ask the agent to return one real record from each
selected provider without combining or interpreting the measurements.

You are done when the agent confirms the operating rules, your actual devices,
and the selected data path. Live integration behavior varies by agent, so use
exports if its MCP or connector setup is unclear.
