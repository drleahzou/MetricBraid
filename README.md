# MetricBraid

**A routing model that makes an AI say "I don't know" about your own body.**

If you wear more than one tracker — a ring and a watch, a band and a chest
strap, a watch and a phone — you have devices producing overlapping,
disagreeing claims about the same physical events.
Wire both into an AI and ask "how am I doing?" and the naive answer is
fluent, confident, and wrong — it double-counts one run as two workouts,
averages two sensors into a number neither one measured, and reports a
sleep-stage breakdown as fact when the underlying validation says otherwise.

MetricBraid is the correction layer: a set of routing rules, evidence
dossiers, and analytical standards that tell the assistant **which source
wins, under which conditions, and how much to trust the answer.**

**It is not an Oura+Garmin tool.** The rules are written against capability
classes; [`devices.yaml`](devices.yaml) binds those classes to whatever you
actually own — Whoop, Apple Watch, Fitbit, Polar, Coros, a chest strap, an
armband, or a single device on its own. The reference setup happens to be a
ring plus a running watch because that is what the author wears; nothing in
the rules depends on it.

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
| **A** | `passive_247` — continuous physiological monitoring | Whichever device you declare as worn 24/7 | 🟡 [**Provisional**](evidence/rule-a-passive.md) |
| **B** | `recorded_workout` — deliberately recorded sessions | The richer recorder for the event; the **best HR sensor class** for heart rate | 🟢 [**Verified**, one open gap](evidence/rule-b-recorded-workouts.md) |
| **C** | `auto_detected` — incidental activity, no matching record | Whichever device detected it | 🟢 [**Verified** for attribution](evidence/rule-c-incidental.md) |
| **D** | Self-reported nutrition | Your own food log | ⚪ Outside the capability model |

**[→ Read the evidence: every study, with methodology and what it doesn't
prove](evidence/)** — ten peer-reviewed papers against polysomnography and
ECG, plus one deliberately not relied upon.

Evidence is split by **how far it generalizes**: `evidence/general/` is
multi-brand or mechanism-based and applies to any wearable you own;
`evidence/devices/` holds per-device numbers that transfer to nothing else.
A device with no dossier still routes correctly — it just inherits the
general baselines and no more.

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
- **[`devices.yaml`](devices.yaml)** — your hardware and what each device
  can do. **The only file most people need to edit.** Ships with commented
  presets for common trackers.
- **[`SETUP.md`](SETUP.md)** — Garmin + Oura authentication, including the
  Oura OAuth2 migration.
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

## Using it with your devices

Edit [`devices.yaml`](devices.yaml). You should not need to touch the rules.

```yaml
devices:
  - name: WHOOP
    capabilities: [passive_247, auto_detected, recorded_workout]
    hr_sensor: wrist_optical        # or optical_armband on the bicep
external_hr_monitors:
  owned:
    - name: Polar Verity Sense
      class: optical_armband
```

Declare which capability classes each device provides and where its HR
sensor sits, and the routing follows. The file ships with commented presets
for Whoop, Apple Watch, Fitbit, Polar, Coros, Suunto and Samsung.

**What works immediately, with any hardware:**
- All routing — capability classes are structural, not empirical
- Deduplication, provenance, and the analytical standards
- The device-agnostic evidence in [`evidence/general/`](evidence/general/):
  the HR placement hierarchy, sleep-tracking limits, step and energy accuracy

**What you'd need to add:** a dossier in
[`evidence/devices/`](evidence/devices/) if you want device-*specific*
accuracy claims — a particular device's HRV offset or staging bias. Start
from [`TEMPLATE.md`](evidence/devices/TEMPLATE.md). Without one, the
assistant is instructed to say so rather than borrow another device's
numbers.

**Edge cases the rules handle explicitly:** a single device (valid — but
confidence goes *down*, since nothing cross-validates), two devices
declaring the same class (`tiebreaks` in `devices.yaml`, and the assistant
must say a tiebreak decided the answer), and three or more devices.

### One honest limitation: data access

The **rules** are device-agnostic. The **plumbing** is not. This repo bundles
MCP servers for Oura and Garmin only, because those are what the author has
wired up. For other hardware you supply the data yourself:

| Your setup | What you get |
|---|---|
| Oura and/or Garmin | Works out of the box — see [SETUP.md](SETUP.md) |
| Another device with a community MCP server | Add it to `.mcp.json` and declare it in `devices.yaml`; the rules don't care where records come from |
| No MCP server available | Paste exports in, or drop a CSV in the repo. The routing, dedup and confidence rules all still apply — this is exactly how Rule D (nutrition) already works, since no food logger has an MCP server either |

Rule D is the proof this degrades gracefully: it is the source of truth for
intake and has *never* had a server behind it.

## License

MIT — see [LICENSE](LICENSE).

**Not medical advice.** This is tooling for personal data analysis. Nothing
here is a diagnostic instrument.
