# MetricBraid

**A routing model that makes an AI say "I don't know" about your own body.**

If you wear an Oura ring and train with a Garmin, you have two devices
producing overlapping, disagreeing claims about the same physical events.
Wire both into an AI and ask "how am I doing?" and the naive answer is
fluent, confident, and wrong — it double-counts one run as two workouts,
averages two sensors into a number neither one measured, and reports a
sleep-stage breakdown as fact when the underlying validation says otherwise.

MetricBraid is the correction layer: a set of routing rules, evidence
dossiers, and analytical standards that tell the assistant **which source
wins, under which conditions, and how much to trust the answer.**

> This is a **template**, not a data repository. No health data is
> published here.

## The core idea: route by capability, not by brand

A rule never says "Oura wins sleep." It says *the passively-worn continuous
sensor wins passive signals* — and each device declares which capability
classes it has. The **record** carries the class, not the device, so an
Oura auto-detected walk routes through Rule C even though Oura also owns
Rule A.

| Rule | Capability class | Source of truth | Status |
|---|---|---|---|
| **A** | `passive_247` — continuous physiological monitoring | The 24/7 passive sensor (here: Oura) | 🟡 [**Provisional**](evidence/rule-a-passive.md) |
| **B** | `recorded_workout` — deliberately recorded sessions | The richer recorder for the event; the **best HR sensor class** for heart rate | 🟢 [**Verified**, one open gap](evidence/rule-b-recorded-workouts.md) |
| **C** | `auto_detected` — incidental activity, no matching record | Whichever device detected it | 🟢 [**Verified** for attribution](evidence/rule-c-incidental.md) |
| **D** | Self-reported nutrition | The user's own food log | ⚪ Outside the capability model |

**[→ Read the evidence: every study, with methodology and what it doesn't
prove](evidence/)** — six peer-reviewed validation papers against
polysomnography and ECG, plus one deliberately not relied upon.

Rule A is marked provisional **and the assistant is required to say so out
loud** whenever it leans on it — because the evidence does not close two
gaps: there is no independent Oura-vs-Garmin head-to-head for passive
signals, and current-generation sleep-staging replication is thin.
[The full reasoning is in the Rule A dossier.](evidence/rule-a-passive.md)

## What's actually in here

- **[`CLAUDE.md`](CLAUDE.md)** — the operating rules. Source-of-truth routing,
  deduplication (±12 min overlap buffer), evidence discipline, analytical
  standards (personal baseline over population norms, confounders, lag
  windows, sample-size honesty).
- **[`evidence/`](evidence/)** — [an index of every paper cited](evidence/README.md),
  plus a dossier per rule ([A](evidence/rule-a-passive.md) ·
  [B](evidence/rule-b-recorded-workouts.md) ·
  [C](evidence/rule-c-incidental.md)) recording methodology, sample size,
  device generation, confidence, and the gaps the evidence leaves open. A
  [`CHANGELOG.md`](evidence/CHANGELOG.md) logs every rule change *including
  reviews that conclude "no change"*, and [`watchlist.yaml`](evidence/watchlist.yaml)
  lists the monitored sources.
- **[`SETUP.md`](SETUP.md)** — Garmin + Oura authentication, including the Oura OAuth2
  migration.
- **[`scripts/oura_auth.py`](scripts/oura_auth.py)** — dependency-free Oura OAuth2 helper.
- **[`plugins/metricbraid/`](plugins/metricbraid/)** — the whole thing packaged as a Claude Code
  plugin.

## Install

### As a Claude Code plugin (recommended)

```
/plugin marketplace add drleahzou/MetricBraid
```

Then install the `metricbraid` plugin. This wires up both MCP servers and
installs the routing skill. Run `/metricbraid-init` in a project to drop in
a `CLAUDE.md` preconfigured with the rules.

### As a template repo

Clone it, then follow [SETUP.md](SETUP.md).

```bash
git clone https://github.com/drleahzou/MetricBraid.git
cd MetricBraid
```

Both paths still require your own Garmin and Oura credentials — see
[SETUP.md](SETUP.md). **Note that Oura Personal Access Tokens were
deprecated in Dec 2025 and newly created ones return 401**; OAuth2 is the
only working path.

## Design commitments

These are the parts that took the longest to get right, and the parts most
worth stealing:

1. **Never average two sensors.** Averaging invents a value neither device
   measured. Pick a winner by rule, absorb the loser, record the merge.
2. **Route channels, not records.** One session can have its pace from one
   device and its heart rate from another. A chest strap paired to the ring's
   app beats a strap-less watch for HR while the watch still owns GPS and
   power — because the strap is the sensor and the watch is only the
   recorder.
3. **Carry provenance on every number.** Which source produced it, which
   rule selected it, what was merged into it, whether the governing rule is
   provisional. If you can't answer that, you can't defend the number.
4. **Never cite a study from memory.** Accuracy claims come from [a dossier
   in `evidence/`](evidence/) or they get read against the primary source
   first.
5. **A new finding is never an automatic rule change.** Raise it, record
   it, then propose the edit — and log it, even when the conclusion is
   "no change."
6. **Personal baseline over population norms.** Given a ~15 ms RMSSD
   underestimate and ~9% step underestimate, a population norm compared
   against a biased absolute number is meaningless. Their own history is
   the only valid reference frame.
7. **Name the weakest number.** Energy expenditure is the least accurate
   metric in the system, from any brand. Never build a conclusion on it.

## Adapting it to other devices

The rules are written around capability classes, not Oura and Garmin
specifically. To swap in a Whoop, an Apple Watch, or a Fitbit: decide which
capability classes the device declares, and the routing follows. What you
*must* redo is [`evidence/`](evidence/) — the dossiers are device-specific, and an
uncited rule is exactly the failure mode this repo exists to prevent.

## License

MIT — see [LICENSE](LICENSE).

**Not medical advice.** This is tooling for personal data analysis. Nothing
here is a diagnostic instrument.
