# Claude Code quick start

This is the easiest and most complete MetricBraid setup. Use it if you work in
Claude Code. You do not need to clone this repository.

## 1. Install

In Claude Code, add the MetricBraid marketplace:

```text
/plugin marketplace add drleahzou/MetricBraid
```

Open the plugin browser and install `metricbraid`.

## 2. Activate and open setup

Run:

```text
/reload-plugins
/metricbraid:metricbraid-init
```

Run init inside the project where you want to use MetricBraid.

## 3. Configure your devices

Answer the setup interview with only the devices you actually wear. It will
create or safely merge the routing instructions, build `devices.yaml`, and
install the setup guide and Oura helper without silently overwriting existing
files.

Declaring a device says what it can measure; it does not claim that its
measurements are accurate. Tiebreaks are optional preferences, not evidence.

## 4. Authenticate selected data sources

Choose only the sources you use. Init checks their prerequisites and walks you
through the relevant steps in `SETUP.md`:

- Oura uses OAuth2 and the included `scripts/oura_auth.py` helper.
- Garmin uses the interactive `garmin-mcp-auth` flow.
- Local or pasted data needs no authentication.

Enter passwords, secrets, tokens, and MFA codes only in your terminal or the
provider's website, never in chat.

After changing credentials or environment variables, fully exit Claude Code
and start a fresh session in the same project.

## 5. Verify

Ask this in the fresh session, removing any provider you did not configure:

> Verify my MetricBraid setup. Pull yesterday's sleep from Oura and
> yesterday's stats from Garmin, then report each connection as ready or
> explain the exact remaining setup step. Do not combine or analyse the
> measurements yet.

You are done when every selected provider returns real data and
`devices.yaml` lists only your actual hardware. For local-only data, you are
done when init reports the project files and device registry ready.

For provider-specific authentication and troubleshooting, use
[`SETUP.md`](../SETUP.md).

## Updating an existing install

Claude Code compares plugin versions using its locally cached marketplace.
Refresh that cache before updating:

```text
/plugin marketplace update metricbraid
/plugin update metricbraid@metricbraid
```

If `/plugin` is unavailable in your environment, use the terminal commands:

```bash
claude plugin marketplace update metricbraid
claude plugin update metricbraid@metricbraid
```

Restart Claude Code afterwards so the new skill and MCP definitions load.

> **Installed before v0.2.0?** Releases through `0.1.0` reused one version
> number, so a normal update can incorrectly report that it is current.
> Reinstall once, then use normal updates for later versions:
>
> ```bash
> claude plugin uninstall metricbraid@metricbraid
> claude plugin install metricbraid@metricbraid
> ```
