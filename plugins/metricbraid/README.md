# MetricBraid for Claude Code

After installing this plugin, run `/reload-plugins`, then run
`/metricbraid:metricbraid-init` inside the project where you want to use
MetricBraid.

The init command:

1. checks only the prerequisites for the data sources you use;
2. installs the routing rules, a safe device registry, this plugin's setup
   guide, and the Oura OAuth helper into your project;
3. asks which devices you actually wear;
4. walks you through authentication without asking you to paste secrets into
   chat; and
5. gives you an exact restart and verification prompt.

The plugin is self-contained. For the manual authentication steps, see
[`SETUP.md`](SETUP.md). The Oura OAuth helper is at
[`scripts/oura_auth.py`](scripts/oura_auth.py).

MetricBraid does not upload health data or pull any health records during
setup. It adds rules for deciding which source governs each measurement,
preserving provenance, and reporting unresolved conflicts rather than silently
averaging sensors.
