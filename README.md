# MetricBraid

**MetricBraid decides which measurement an AI is allowed to believe — and
records why.**

It is a provenance and conflict-resolution layer for AI analysis of
overlapping personal sensor data: the routing rules, evidence dossiers and
output contract that sit between a pile of disagreeing device records and an
answer a person acts on.

If you wear more than one tracker — a ring and a watch, a band and a chest
strap, a watch and a phone — you have devices producing overlapping,
disagreeing claims about the same physical events. Wire them into an AI and
ask "how am I doing?" and the naive answer is fluent, confident, and wrong:
it double-counts one run as two workouts, averages two sensors into a number
neither one measured, and reports a sleep-stage breakdown as fact when the
underlying validation says otherwise.

**A routing model that makes an AI say "I don't know" about your own body.**

## What it actually does

```
candidate observations → routing / arbitration → confidence → provenance → answer
```

Every record from every configured source is a candidate. Routing decides
which source governs which claim. Confidence is graded on two independent
axes. Provenance is carried on every number in a canonical form. What is
material reaches the answer — including "no rule resolves this, here are
both values."

**It is not an Oura+Garmin tool.** The rules are written against capability
classes; [`devices.yaml`](devices.yaml) binds those classes to whatever you
actually own — Whoop, Apple Watch, Fitbit, Polar, Coros, a chest strap, an
armband, or a single device on its own. The bundled MCP plumbing currently
covers Oura and Garmin because that is what the author has wired up; the
routing model does not depend on them. See
[the data-access limitation](#one-honest-limitation-data-access).

> This is a **template**, not a data repository. No health data is
> published here.

## Three layers, kept apart

The first thing to know is which file you are looking at.

| Layer | Files | Defines | You edit it when |
|---|---|---|---|
| **Framework** | [`CLAUDE.md`](CLAUDE.md), [`spec/`](spec/) | Capability classes, routing rules, channel arbitration, deduplication, the two confidence axes, provenance, evidence discipline, analytical standards | The model itself improves |
| **User configuration** | [`devices.yaml`](devices.yaml), `.mcp.json`, credentials | Your devices, which capability classes each declares, HR sensor placement, tiebreak preferences, external monitors, known provider defects | Your hardware or setup changes |
| **Evidence** | [`evidence/`](evidence/) | Device-agnostic baselines, device-specific claims, rule-level reasoning, open gaps, confidence limits | New validation is published |

**Most people only ever edit `devices.yaml`.** The rules name no hardware; if
a rule starts naming a brand to pick a winner, that is a bug in the rule.

## The core idea: route by capability, not by brand

A rule never says "the ring wins sleep." It says *the passively-worn
continuous sensor governs passive signals* — and each device declares which
capability classes it has. The **record** carries the class, not the device,
so an auto-detected walk from a device that also does passive monitoring
still routes through Rule C.

| Rule | Capability class | Governing source | Routing basis | Measurement confidence |
|---|---|---|---|---|
| **A** | `passive_247` — continuous physiological monitoring | Whichever device you declare as worn 24/7 | 🟡 [`provisional`](evidence/rule-a-passive.md) — reasoned, not measured | Duration `high` · staging `low` · HRV `moderate` as trend |
| **B** `event` | `recorded_workout` — GPS, pace, power, load | The record that captured the channel | 🟢 [`structural`](evidence/rule-b-recorded-workouts.md) | `high` |
| **B** `heart_rate` | The **best HR sensor class** present, whoever recorded | Strap or armband over wrist over ring | 🟢 [`evidence_backed`](evidence/rule-b-recorded-workouts.md) | Set by sensor class and intensity |
| **C** | `auto_detected` — incidental activity, no matching record | Whichever device detected it | 🟢 [`structural`](evidence/rule-c-incidental.md) — sole detector | Steps `moderate` · energy `unusable` |
| **D** | Self-reported intake | Your own food log | ⚪ Outside the capability model | Graded by how it was captured |

### Two confidences, never collapsed

The distinction the whole model turns on: **knowing which source owns a
number tells you nothing about whether the number is any good.**

- Rule C attributes an incidental walk with total certainty — nothing else
  saw it — and grades its calorie figure `unusable`.
- Rule A's sleep-duration *measurement* is well validated; the claim that a
  ring-class device should *own* it is not.
- A `tiebreaks` entry resolves routing deterministically and improves
  measurement confidence by exactly nothing. The assistant has to say a
  preference decided the answer.

`unvalidated` is also not `low`. `low` means studied and found poor, so you
can say how wrong it probably is; `unvalidated` means nobody looked. That is
why an unstudied ring sensor never displaces a known-imperfect wrist sensor
when no strap is worn.

**[→ Read the evidence: every study, with methodology and what it doesn't
prove](evidence/)** — ten peer-reviewed papers against polysomnography and
ECG, plus one deliberately not relied upon.

Evidence is split by **how far it generalizes**: `evidence/general/` is
multi-brand or mechanism-based and applies to any wearable you own;
`evidence/devices/` holds per-device numbers that transfer to nothing else.
A device with no dossier still routes correctly — it just inherits the
general baselines and no more.

## What's actually in here

- **[`CLAUDE.md`](CLAUDE.md)** — the operating spec. Routing, channel
  arbitration, deduplication (±12 min overlap buffer), provenance
  requirements, evidence discipline, analytical standards (personal baseline
  over population norms, confounders, lag windows, sample-size honesty).
- **[`spec/`](spec/)** — the [routed observation](spec/routed-observation.md):
  the canonical form every routed metric takes, with a
  [JSON Schema](spec/routed-observation.schema.json) and
  [worked examples](spec/examples/) covering a channel split, an unresolved
  conflict, and a withheld observation.
- **[`evidence/`](evidence/)** — [an index of every paper cited](evidence/README.md),
  plus a dossier per rule ([A](evidence/rule-a-passive.md) ·
  [B](evidence/rule-b-recorded-workouts.md) ·
  [C](evidence/rule-c-incidental.md)) recording methodology, sample size,
  device generation, both confidence grades, and the gaps the evidence
  leaves open. A [`CHANGELOG.md`](evidence/CHANGELOG.md) logs every rule
  change *including reviews that conclude "no change"*, and
  [`watchlist.yaml`](evidence/watchlist.yaml) lists the monitored sources,
  checked weekly by [`scripts/evidence_watch.py`](scripts/evidence_watch.py),
  which opens an issue for a human to triage and never edits a rule itself.
- **[`fixtures/`](fixtures/)** — twelve adversarial routing cases with
  expected outcomes, so the behaviour that matters survives a prompt or model
  change. Structure-checked by
  [`check_fixtures.py`](fixtures/check_fixtures.py).
- **[`devices.yaml`](devices.yaml)** — your hardware and what each device
  can do. **The only file most people need to edit.** Ships with commented
  presets for common trackers.
- **[`SETUP.md`](SETUP.md)** — authentication for the two bundled
  integrations, including the Oura OAuth2 migration.
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
a `CLAUDE.md` preconfigured with the rules and a `devices.yaml` to fill in.

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
   measured. Select by rule, absorb the loser, record the merge. Where no
   rule decides, report both and say nothing resolved it — a selected source
   is the one a rule designated, not the one shown to be right.
2. **Route channels, not records.** One session can have its pace from one
   device and its heart rate from another. A strap paired to a ring's app
   beats a strap-less watch for HR while the watch still owns GPS and power —
   because the strap is the sensor and the watch is only the recorder.
3. **Carry provenance in a canonical form.** Every routed metric is a
   [routed observation](spec/routed-observation.md): source, sensor, rule,
   basis, confidence, evidence, what was merged, what has to be disclosed.
   If you can't fill that in, you can't defend the number.
4. **Separate routing confidence from measurement confidence.** They are
   different questions and they move independently. Collapsing them is how a
   routing decision starts sounding like a validated one.
5. **Never cite a study from memory.** Accuracy claims come from [a dossier
   in `evidence/`](evidence/) or they get read against the primary source
   first.
6. **A new finding is never an automatic rule change.** Raise it, record
   it, then propose the edit — and log it, even when the conclusion is
   "no change."
7. **Personal baseline over population norms.** Given a ~15 ms RMSSD
   underestimate and ~9% step underestimate, a population norm compared
   against a biased absolute number is meaningless. Their own history is
   the only valid reference frame.
8. **Name the weakest number.** Energy expenditure is the least accurate
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
numbers. Adding a dossier never promotes a device in the routing; it only
changes what may be said about its numbers.

**Edge cases the rules handle explicitly:** a single device (valid — but
confidence goes *down*, since nothing cross-validates), two devices
declaring the same class (`tiebreaks` in `devices.yaml`, and the assistant
must say a tiebreak decided the answer), an unset tiebreak (report both, pick
neither), and a metric that fits no rule (flag it and ask, don't guess).

### One honest limitation: data access

The **rules** are device-agnostic. The **plumbing** is not. This repo bundles
MCP servers for Oura and Garmin only, because those are what the author has
wired up. For other hardware you supply the data yourself:

| Your setup | What you get |
|---|---|
| Oura and/or Garmin | Works out of the box — see [SETUP.md](SETUP.md) |
| Another device with a community MCP server | Add it to `.mcp.json` and declare it in `devices.yaml`; the rules don't care where records come from |
| No MCP server available | Paste exports in, or drop a CSV in the repo. The routing, dedup and confidence rules all still apply — this is exactly how Rule D (nutrition) already works, since no food logger has an MCP server either |

Rule D is the proof this degrades gracefully: it governs intake and has
*never* had a server behind it.

## License

MIT — see [LICENSE](LICENSE).

**Not medical advice.** This is tooling for personal data analysis. Nothing
here is a diagnostic instrument — much of what the framework does is
establish how *little* some numbers support.
