# MetricBraid

**MetricBraid decides which measurement an AI is allowed to believe and records why.**

MetricBraid is an open-source framework for AI analysis of overlapping wearable health and sensor data, with source routing, deduplication, confidence grading, and provenance.

Connect your wearable and sensor data to an AI agent, then ask questions about your sleep, recovery, activity, training, or health trends without first having to reconcile conflicting devices yourself.

If your ring says you slept 7h 42m, your watch says 7h 05m, both recorded yesterday's run, and a chest strap captured the better heart-rate signal, MetricBraid determines which source should govern each part of the analysis, removes duplicates, grades how trustworthy each measurement is, and preserves why each number was selected.

It sits between your sensor observations and the answer your AI gives you.

---

# Choose your setup

Choose the application you will use, not the underlying model. Each guide
shows only the steps for that environment and ends with an exact verification
prompt.

| I am using | Best current route | Start here |
|---|---|---|
| **Claude Code** | Install the MetricBraid plugin; no repository clone required | [Claude Code quick start](docs/2026-08-31-claude-code-quick-start.md) |
| **Codex** | Clone the repository and let its `AGENTS.md` guide Codex | [Codex quick start](docs/2026-08-31-codex-quick-start.md) |
| **Gemini CLI, Cursor, or another agent** | Clone the portable framework and provide its project instructions | [Other agents quick start](docs/2026-08-31-other-agents-quick-start.md) |
| **Any agent with exports or pasted observations** | Skip live integrations and provide local files | [Local-data quick start](docs/2026-08-31-local-data-quick-start.md) |

If you already use Claude Code, choose that route: it has the most complete
packaged setup. If you do not need live wearable connections, the local-data
route has the fewest authentication steps.

`SETUP.md` is the shared reference for device configuration, Oura and Garmin
authentication, security, and troubleshooting. Start with one quick start
above rather than reading the entire reference from top to bottom.

---

## Why this exists

If you use more than one tracker — a ring and a watch, a band and a chest strap, a watch and a phone — you have devices producing overlapping and sometimes contradictory claims about the same physical events.

Give all of those records to an AI and ask:

> "How am I doing?"

and the naive answer can be fluent, confident, and wrong.

It might:

* count one run as two workouts;
* average two sensors into a value neither device actually measured;
* use wrist heart rate even though a chest strap captured the same session;
* compare measurements with different known biases as though they were equivalent;
* report sleep-stage estimates as physiological fact;
* build conclusions on calorie estimates that are too inaccurate to support them;
* silently pick one device when there is no defensible reason to prefer it.

MetricBraid sits between the raw observations and the analysis:

```text
candidate observations
        ↓
routing / arbitration
        ↓
confidence
        ↓
provenance
        ↓
analysis
        ↓
answer
```

Every observation from every configured source starts as a candidate.

MetricBraid determines:

1. which source governs each claim;
2. whether overlapping records represent the same physical event;
3. which sensor should govern individual channels such as heart rate;
4. how confident the system is in the routing decision;
5. how trustworthy the underlying measurement actually is;
6. what evidence supports those judgements;
7. what uncertainty must remain visible in the final answer.

If no rule resolves a conflict, MetricBraid does not quietly choose a winner.

It reports the disagreement and says that the conflict is unresolved.

---

# What you can do with it

Once MetricBraid and your data sources are available to an AI agent, you query your data naturally.

You do not need to manually decide which tracker to trust before asking the question.

For example:

* **"How has my recovery changed over the last month?"**
* **"Am I sleeping better than I was six weeks ago?"**
* **"What happened to my resting heart rate after I increased my running volume?"**
* **"Compare the two records of yesterday's run."**
* **"Which heart-rate data should I trust for this workout, and why?"**
* **"Was that walk recorded twice across my devices?"**
* **"Show me the trend in my HRV, but tell me which measurements are actually comparable."**
* **"What changed in the week before my race?"**
* **"How has my training load changed over the last eight weeks?"**
* **"Which recent conclusions depend on low-confidence measurements?"**
* **"Show me my sleep trend, but don't overinterpret sleep stages."**
* **"Did my resting heart rate change before my performance dropped?"**
* **"Which measurements in this analysis are least trustworthy?"**
* **"Explain exactly where each number in this conclusion came from."**

MetricBraid operates underneath those questions.

Before the AI analyses the data, the framework determines which observations should be used, which should be merged or withheld, how much confidence should be attached to them, and what provenance needs to follow each number into the answer.

So instead of getting something like:

> "You completed 12 workouts this week and burned 5,840 calories."

from two trackers that both recorded the same six sessions, MetricBraid gives the agent enough structure to produce something closer to:

> "You completed 6 distinct workouts. The watch record governs GPS and pace for these sessions, while the chest strap governs workout heart rate. The overlapping records from your second device were treated as duplicates. I would not use the combined calorie estimate for a conclusion because energy expenditure is low-confidence across these sensors."

The goal is not simply to give an AI access to more health data.

It is to make the AI **reason about overlapping sensor data before reasoning from it**.

---

# Agent-agnostic by design

MetricBraid's core framework is not tied to one model, vendor, or coding agent.

The following are portable:

* routing rules;
* capability classes;
* conflict-resolution logic;
* deduplication rules;
* channel arbitration;
* routing confidence;
* measurement confidence;
* provenance requirements;
* evidence dossiers;
* routed-observation schemas;
* test fixtures;
* device configuration.

Any sufficiently capable agent that can read the framework and access the underlying observations can apply the model.

The current repository includes **Claude Code packaging as the easiest reference implementation**, but Claude is not part of the routing model itself.

Conceptually:

```text
                    MetricBraid core
                           │
          ┌────────────────┼────────────────┐
          │                │                │
     Claude Code          Codex        other agents
          │                │                │
          └──────── platform adapters ──────┘
```

Platform-specific packaging may differ.

The reasoning model should not.

---

# Supported AI agents

## Claude Code

Claude Code has the most complete packaged setup: an installable plugin,
interactive device interview, bundled references and MCP configuration, and a
defined readiness check. Follow the
[Claude Code quick start](docs/2026-08-31-claude-code-quick-start.md).

---

## Codex

The cloned repository includes an [`AGENTS.md`](AGENTS.md) adapter that tells
Codex when to load the canonical framework and how to handle setup safely.
Live integrations require Codex-specific MCP configuration; local files do
not. Follow the [Codex quick start](docs/2026-08-31-codex-quick-start.md).

---

## Other agents

Gemini CLI, Cursor, other MCP-capable tools and custom agents can use the same
framework, but they do not yet have a packaged MetricBraid installer. Follow
the [other agents quick start](docs/2026-08-31-other-agents-quick-start.md), or
use the [local-data route](docs/2026-08-31-local-data-quick-start.md) for the
smallest setup surface.

---

# Supported devices

MetricBraid's **routing model is device-agnostic**.

Rules operate on capability classes rather than brand names.

[`devices.yaml`](devices.yaml) maps those capability classes onto the hardware you actually own.

That means the framework can describe hardware such as:

* Garmin;
* Oura;
* WHOOP;
* Apple Watch;
* Fitbit;
* Polar;
* Coros;
* Suunto;
* Samsung;
* chest straps;
* optical armbands;
* phones;
* a single wearable on its own.

The bundled data integrations currently cover **Oura and Garmin**, because those are the integrations currently wired into this repository.

Other devices can still participate if you provide their observations through:

* another MCP server;
* an API;
* an export;
* CSV;
* structured files;
* another compatible integration.

See [Data access](#data-access).

> **This repository is a template and framework, not a health-data repository. No personal health data is published here.**

---

# Installation and setup

Use the [setup chooser](#choose-your-setup) rather than combining instructions
from several platforms. Every quick start follows the same sequence:

```text
install → activate or open → configure devices → connect or provide data → verify
```

The quick starts contain the commands and prompts to copy. Use
[`SETUP.md`](SETUP.md) only when a selected provider needs authentication or
when you are troubleshooting.

> **Oura note:** Personal Access Tokens were deprecated in December 2025.
> Newly created PATs return `401`; OAuth2 is the supported authentication path.

---

# How MetricBraid works

## Route by capability, not by brand

MetricBraid does not contain rules such as:

> "Oura wins sleep."

or:

> "Garmin wins workouts."

Instead, rules describe the measurement capability that should govern a particular claim.

For example:

> *The passively worn continuous sensor governs passive signals.*

or:

> *The best available heart-rate sensor class governs workout heart rate.*

Each device declares its capabilities in [`devices.yaml`](devices.yaml).

The **observation carries the capability class**, not the brand.

That distinction matters because one device may generate several fundamentally different kinds of observation.

A watch might provide:

* continuous passive monitoring;
* explicitly recorded workouts;
* auto-detected incidental activity.

Those observations should not all route the same way simply because they came from the same hardware.

---

# Core routing rules

| Rule               | Capability class                                              | Governing source                          | Routing basis                                                           | Measurement confidence                                    |
| ------------------ | ------------------------------------------------------------- | ----------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------- |
| **A**              | `passive_247` — continuous physiological monitoring           | Whichever device you declare as worn 24/7 | 🟡 [`provisional`](evidence/rule-a-passive.md) — reasoned, not measured | Duration `high` · staging `low` · HRV `moderate` as trend |
| **B** `event`      | `recorded_workout` — GPS, pace, power, load                   | The record that captured the channel      | 🟢 [`structural`](evidence/rule-b-recorded-workouts.md)                 | `high`                                                    |
| **B** `heart_rate` | Best HR sensor class present                                  | Strap or armband over wrist over ring     | 🟢 [`evidence_backed`](evidence/rule-b-recorded-workouts.md)            | Set by sensor class and intensity                         |
| **C**              | `auto_detected` — incidental activity with no matching record | Whichever device detected it              | 🟢 [`structural`](evidence/rule-c-incidental.md) — sole detector        | Steps `moderate` · energy `unusable`                      |
| **D**              | Self-reported intake                                          | Your own food log                         | ⚪ Outside the capability model                                          | Graded by capture method                                  |

---

# Two kinds of confidence

The distinction MetricBraid turns on is simple:

> **Knowing which source owns a number tells you nothing about whether the number itself is any good.**

MetricBraid therefore keeps two confidence questions separate.

## Routing confidence

How confident are we that this observation is the correct source to govern the claim?

## Measurement confidence

How trustworthy is the measurement itself?

These can move independently.

For example:

* Rule C can attribute an incidental walk with certainty because only one device detected it while grading its calorie estimate `unusable`.
* Rule A's sleep-duration measurement can be reasonably well validated while the claim that a particular capability class should own the observation remains provisional.
* A `tiebreaks` entry can resolve routing deterministically while improving measurement confidence by exactly nothing.

If a user-configured preference breaks a tie, the AI must disclose that a preference decided the result.

---

# `unvalidated` does not mean `low`

MetricBraid distinguishes between:

## `low`

The measurement has been studied and found to perform poorly.

## `unvalidated`

There is not enough relevant evidence to know how well it performs.

Those are not interchangeable.

A known-imperfect measurement may sometimes be more defensible than an entirely unstudied one because at least its error characteristics are understood.

That is why an unvalidated sensor does not automatically displace a known-imperfect sensor merely because it appears newer, more precise, or more sophisticated.

---

# Evidence

MetricBraid deliberately separates its evidence model from its routing model.

**[→ Browse the evidence library](evidence/)**

The repository includes peer-reviewed validation evidence against reference standards such as polysomnography and ECG, alongside explicit notes about what each study does **not** establish.

Evidence is divided according to how far a finding can reasonably generalise.

---

## General evidence

[`evidence/general/`](evidence/general/)

Contains multi-brand, sensor-class, mechanism-level, or otherwise generalisable evidence.

Examples include:

* heart-rate sensor placement;
* sleep-tracking limitations;
* step-count accuracy;
* energy-expenditure limitations.

These findings may apply across multiple devices where the mechanism supports that generalisation.

---

## Device-specific evidence

[`evidence/devices/`](evidence/devices/)

Contains findings that should **not** automatically transfer to another device.

Examples include:

* a particular model's HRV offset;
* device-specific heart-rate bias;
* sleep-stage performance;
* generation-specific validation results.

A device without its own dossier can still route correctly.

It simply inherits applicable general evidence and no more.

The agent is instructed to disclose the missing validation rather than borrow numbers from another device.

---

# Three layers, kept separate

MetricBraid separates the framework, user configuration, and evidence.

| Layer                  | Files                                                         | Defines                                                                                                                                  | You edit it when                 |
| ---------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| **Framework**          | operating spec, [`spec/`](spec/)                              | Capability classes, routing rules, channel arbitration, deduplication, confidence, provenance, evidence discipline, analytical standards | The model itself improves        |
| **User configuration** | [`devices.yaml`](devices.yaml), MCP/config files, credentials | Your devices, capability classes, HR sensor placement, tiebreak preferences, external monitors, known provider defects                   | Your hardware or setup changes   |
| **Evidence**           | [`evidence/`](evidence/)                                      | General baselines, device-specific claims, rule-level reasoning, open gaps, confidence limits                                            | New validation becomes available |

**Most people should only need to edit `devices.yaml`.**

A platform adapter may generate additional agent-specific instruction files.

Those should not become independent copies of the framework logic.

---

# Configure your devices

Edit [`devices.yaml`](devices.yaml).

You should not need to modify the routing rules.

For example:

```yaml
devices:
  - name: WHOOP
    capabilities:
      - passive_247
      - auto_detected
      - recorded_workout
    hr_sensor: wrist_optical

external_hr_monitors:
  owned:
    - name: Polar Verity Sense
      class: optical_armband
```

Declare:

* which devices you own;
* which capability classes they provide;
* where their heart-rate sensors sit;
* any external HR monitors;
* any explicit tiebreak preferences.

MetricBraid then routes observations according to the framework.

The supplied configuration includes commented presets for common devices.

---

# What works with any hardware

The following parts of MetricBraid are structural and do not require a device-specific evidence dossier:

* capability-based routing;
* duplicate detection;
* provenance;
* source arbitration;
* channel-level routing;
* analytical standards;
* general evidence;
* HR sensor-placement hierarchy;
* general sleep-tracking limitations;
* general step-count limitations;
* general energy-expenditure limitations.

---

# What requires device-specific evidence

If you want the AI to make claims such as:

> "This device underestimates RMSSD by approximately X%."

or:

> "This specific model's sleep staging performs at approximately Y accuracy."

then that device needs its own evidence dossier.

Create one under:

[`evidence/devices/`](evidence/devices/)

using:

[`evidence/devices/TEMPLATE.md`](evidence/devices/TEMPLATE.md)

Adding a device dossier changes what the agent may defensibly say about that device's measurements.

It does **not** automatically promote the device in the routing hierarchy.

Routing preference and measurement validity remain separate.

---

# Edge cases

MetricBraid explicitly handles cases that otherwise tend to produce plausible but misleading AI answers.

## One device only

Valid.

MetricBraid still routes the data.

The absence of independent observations simply means some conclusions have less opportunity for cross-validation.

---

## Two devices claiming the same capability

Use `tiebreaks` in [`devices.yaml`](devices.yaml).

The AI must disclose that a configured preference resolved the conflict.

---

## No tiebreak configured

Report both values.

Pick neither.

---

## A metric matches no rule

Flag it.

Do not silently map it to whichever existing rule seems closest.

---

## Two devices record the same workout

Deduplicate the event instead of counting two workouts.

Individual channels may still come from different sensors.

---

## External HR sensor used during a workout

Route the heart-rate channel according to the sensor that actually measured it.

The device or app storing the record is not necessarily the physiological sensor.

---

# Route channels, not whole records

A single workout does not necessarily have one universally correct source.

For example:

```text
GPS / pace       → watch
power            → watch
heart rate       → chest strap
workout identity → merged event
```

If a chest strap is paired with another device's app, the strap can govern heart rate while a watch governs GPS and power.

The recording application is not the measurement source.

MetricBraid therefore routes **channels**, not simply files, apps, or device records.

---

# Provenance

Every routed measurement is represented in a canonical form called a:

**[routed observation](spec/routed-observation.md)**

It carries information such as:

* source;
* sensor;
* routing rule;
* routing basis;
* routing confidence;
* measurement confidence;
* supporting evidence;
* merged observations;
* required disclosures.

The schema is defined in:

[`spec/routed-observation.schema.json`](spec/routed-observation.schema.json)

Worked examples are available in:

[`spec/examples/`](spec/examples/)

including:

* channel splitting;
* unresolved conflicts;
* withheld observations.

The basic rule is:

> **If the agent cannot explain where a number came from and why it was selected, it should not build a conclusion on that number.**

---

# Repository structure

## Operating specification

The operating specification defines:

* routing rules;
* capability classes;
* channel arbitration;
* deduplication;
* provenance requirements;
* evidence discipline;
* confidence rules;
* analytical standards.

Analytical standards include:

* personal baseline over population norms;
* confounder awareness;
* lag windows;
* sample-size honesty.

The Claude Code adapter exposes this through `CLAUDE.md`. The root
[`AGENTS.md`](AGENTS.md) gives Codex a small platform-specific entry point and
directs it back to the same canonical specification when MetricBraid applies.

Other agent adapters may expose the same specification through different
platform-specific instruction files.

---

## [`docs/`](docs/)

Environment-specific quick starts for Claude Code, Codex, other agents, and
local files. Each guide covers the same five-stage journey while hiding steps
that do not apply to that environment.

---

## [`AGENTS.md`](AGENTS.md)

The Codex adapter. Codex loads it automatically when the repository is opened;
it keeps setup and analysis scoped to the canonical rules in `CLAUDE.md`,
`devices.yaml`, `spec/`, and `evidence/`.

---

## [`spec/`](spec/)

The routed-observation contract.

Includes:

* the canonical routed-observation definition;
* JSON Schema;
* worked examples.

---

## [`evidence/`](evidence/)

The evidence system.

Includes:

* an [index of cited evidence](evidence/README.md);
* general evidence;
* device-specific evidence;
* rule-level dossiers;
* methodology;
* sample size;
* device generation;
* confidence grading;
* unresolved gaps.

A [`CHANGELOG.md`](evidence/CHANGELOG.md) records every rule review, including reviews that conclude:

> "no change"

[`watchlist.yaml`](evidence/watchlist.yaml) defines monitored evidence sources.

[`scripts/evidence_watch.py`](scripts/evidence_watch.py) checks the watchlist weekly.

When something potentially relevant appears, the process opens an issue for human review.

It **never edits a routing rule automatically**.

---

## [`fixtures/`](fixtures/)

Adversarial routing cases with expected outcomes.

These exist so that the behaviour that matters survives changes to:

* prompts;
* implementations;
* models;
* agent platforms.

Fixture structure is checked by:

[`fixtures/check_fixtures.py`](fixtures/check_fixtures.py)

---

## [`devices.yaml`](devices.yaml)

Your hardware configuration.

For most users, this is the main file you edit.

---

## [`SETUP.md`](SETUP.md)

The shared device, authentication, security, and troubleshooting reference.
Users start with a platform quick start and open this only for the provider
sections they need.

Includes the Oura OAuth2 flow.

---

## [`scripts/`](scripts/)

Utility scripts including:

* [`oura_auth.py`](scripts/oura_auth.py) — dependency-free Oura OAuth2 helper;
* [`evidence_watch.py`](scripts/evidence_watch.py) — weekly evidence-watch process;
* [`sync_plugin.py`](scripts/sync_plugin.py) — keeps generated copies synchronised with canonical repository files.

---

## [`plugins/metricbraid/`](plugins/metricbraid/)

The Claude Code plugin adapter.

It packages MetricBraid into the structure Claude Code expects.

The plugin is a distribution mechanism for the framework.

It is not the framework itself.

---

# One canonical framework

Agent integrations often require their own local instruction files, references, templates, or packaging.

MetricBraid should not maintain separate versions of the reasoning model for every platform.

Conceptually:

```text
canonical MetricBraid specification
             ↓
       platform adapters
       /      |      \
Claude Code  Codex   others
```

The repository-root framework files are canonical.

Platform-specific adapters should point back to those files or generate any
required copies from them.

The existing Claude Code plugin already follows this principle.

A Claude Code plugin must be self-contained, so its skill reads local
`references/` and `/metricbraid:metricbraid-init` copies local templates,
setup instructions and the Oura OAuth helper.

That means some framework content necessarily appears both at the repository root and under the plugin directory.

Those copies are **not maintained independently**.

The Codex [`AGENTS.md`](AGENTS.md) adapter takes the other route: it remains
small and directs Codex to read the canonical files when MetricBraid applies.

[`scripts/sync_plugin.py`](scripts/sync_plugin.py) regenerates them from the canonical repository files.

Run:

```bash
python3 scripts/sync_plugin.py
```

after changing a canonical file.

CI checks synchronisation using:

```bash
python3 scripts/sync_plugin.py --check
```

Editing generated files directly under `plugins/` will be overwritten.

Future agent adapters should likewise point back to the canonical framework or
generate unavoidable packaged copies rather than maintaining another reasoning
model by hand.

---

# Design commitments

These are the principles MetricBraid is built around.

## 1. Never average two sensors

Averaging conflicting observations creates a value that neither sensor actually measured.

Select according to a rule.

Absorb the duplicate.

Record the merge.

If no rule decides, report both.

---

## 2. Route channels, not records

One workout may legitimately use:

* pace from one sensor;
* heart rate from another;
* power from another.

The best source can differ by channel.

---

## 3. Carry provenance

Every material measurement should retain:

* where it came from;
* what captured it;
* why it was selected;
* what was discarded;
* what confidence applies;
* what evidence supports the decision.

If you cannot reconstruct that chain, you cannot defend the number.

---

## 4. Keep routing confidence and measurement confidence separate

They answer different questions.

A measurement can be:

* confidently routed but poorly measured;
* ambiguously routed but accurately measured;
* confidently routed and accurately measured;
* uncertain on both axes.

Do not collapse those states into one score.

---

## 5. Never cite validation evidence from memory

Accuracy claims must come from an evidence dossier or be checked against the underlying source.

An AI sounding familiar with a paper is not evidence.

---

## 6. New evidence does not automatically change a rule

A finding is:

```text
identified
    ↓
reviewed
    ↓
recorded
    ↓
rule change proposed if warranted
```

The result is logged even when the conclusion is:

> "no change"

---

## 7. Prefer personal baselines over population norms

Consumer sensors can have systematic biases.

A population reference range compared with a biased absolute measurement can create false precision.

Whenever possible, MetricBraid prioritises change relative to the same person's own historical measurements.

---

## 8. Name the weakest number

Energy expenditure is one of the least reliable measurements produced by consumer wearables.

MetricBraid does not quietly give a weak number analytical importance simply because a device reports it to the nearest calorie.

If the weakest measurement materially affects the conclusion, the answer should say so.

---

# Data access

There is an important distinction:

**The framework is device-agnostic.
The bundled data plumbing is not.**

This repository currently bundles integrations for **Oura and Garmin**.

For other hardware, provide observations through another route.

| Your setup                                      | What you get                                                                                                                      |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Oura and/or Garmin**                          | Bundled integration — see [`SETUP.md`](SETUP.md)                                                                                  |
| **Another device with a compatible MCP server** | Add the integration, declare the device in `devices.yaml`, and use the same routing rules                                         |
| **Direct API access**                           | Supply the records to the agent and apply the same framework                                                                      |
| **No live integration available**               | Provide an export, CSV, or other structured input; routing, deduplication, confidence, provenance, and analysis rules still apply |

MetricBraid does not require every source to have a live API connection.

Rule D demonstrates this already: self-reported intake can participate in the analysis without a dedicated food-logging MCP server.

The framework governs observations.

It does not care whether those observations arrived through:

* MCP;
* API;
* CSV;
* exported files;
* pasted structured data;
* another compatible integration.

---

# What MetricBraid is not

MetricBraid is not:

* a wearable;
* a health-data warehouse;
* a replacement for Garmin, Oura, WHOOP, Apple Watch, or another tracker;
* an algorithm that mathematically blends multiple devices into a supposedly "more accurate" number;
* a Claude-only project;
* a medical device;
* a diagnostic system.

It is an **agent-agnostic reasoning, provenance, and conflict-resolution framework for overlapping sensor observations**.

Claude Code is currently the easiest packaged implementation.

The framework itself is portable.

---

# Contributing

Contributions are welcome, particularly around:

* new device evidence dossiers;
* general sensor-validation evidence;
* adversarial routing fixtures;
* additional data integrations;
* agent adapters;
* evidence-quality improvements;
* edge cases not currently represented in the framework.

A new integration should not require changing the underlying routing model simply because it introduces a new brand.

A new agent adapter should not maintain an independent version of the MetricBraid rules.

The abstraction is part of the contract.

---

# License

MIT — see [`LICENSE`](LICENSE).

---

## Medical disclaimer

**Not medical advice.**

MetricBraid is tooling for personal data analysis, not a diagnostic instrument.

A substantial part of the framework exists specifically to establish how little some consumer-sensor measurements are capable of supporting.
