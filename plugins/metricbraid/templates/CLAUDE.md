# MetricBraid — Personal Sensor Evidence Router

**MetricBraid decides which measurement an AI is allowed to believe — and
records why.**

When several devices observe the same body, they produce overlapping,
disagreeing claims about the same physical events. This file is the operating
specification for resolving that: which source governs which signal, how
competing records are collapsed without inventing values, how much confidence
survives, and what has to be said out loud.

Every session in this project MUST follow these rules without being re-told.

## What this file is, and what it is not

Three layers, deliberately separated. Know which one you are reading before
changing anything.

| Layer | File(s) | Defines | Changes when |
|---|---|---|---|
| **Framework** | this file, and the routed-observation contract ([`spec/`](https://github.com/drleahzou/MetricBraid/blob/main/spec/)) | Capability classes, routing rules, channel arbitration, deduplication, the two confidence axes, provenance requirements, evidence discipline, analytical standards | The model itself improves |
| **User configuration** | [`devices.yaml`](devices.yaml), `.mcp.json`, credentials | Which devices exist, which capability classes each declares, where its HR sensor sits, tiebreak preferences, external monitors, known provider defects, integrations | The user's hardware or setup changes |
| **Evidence** | the plugin skill's `references/` ([online](https://github.com/drleahzou/MetricBraid/blob/main/evidence/)) | Device-agnostic baselines, device-specific claims, rule-level reasoning, open gaps, confidence limits | New validation is published or a device generation ships |

**This file names no hardware in its rules.** It routes by capability class.
`devices.yaml` binds classes to actual devices. If a rule here starts naming a
brand to pick a winner, that is a bug in the rule.

Concrete brands appear only in: the bundled integrations and authentication
section at the end, examples explicitly marked as drawn from the reference
configuration, and the per-device dossiers in `evidence/devices/`.

## The pipeline

```
candidate observations → routing / arbitration → confidence → provenance → answer
```

1. **Candidate observations** — every record from every configured source that
   could bear on the question, before any filtering.
2. **Routing / arbitration** — capability class and channel decide which source
   governs each claim. Overlapping records for one real-world event are
   collapsed, never summed and never averaged.
3. **Confidence** — two independent grades: how firmly the source was selected,
   and how much its number is worth.
4. **Provenance** — the routed observation carries source, rule, basis,
   confidence, evidence, and everything absorbed along the way.
5. **Answer** — the material parts of that provenance reach the user. A number
   whose provenance cannot be stated cannot be defended, and should not be
   reported.

## READ `devices.yaml` FIRST

Read it at the start of any analysis session and route from what it declares —
never from what you assume the user owns, and never from which MCP servers
happen to respond.

- If `devices.yaml` is missing, or a device is not listed, **say so and ask**
  rather than inferring hardware.
- A device's presence declares **capabilities only**. It confers no accuracy
  claim. Accuracy comes only from a dossier in `evidence/`.
- If a configured integration is unavailable, **say so before analysing.**
  Never substitute assumptions for missing tool output, and never let a
  silently absent source change a routing outcome without saying it did.

### Devices with no dossier

Most devices will not have one. That is expected and is not a blocker — it
changes what you may *say*, not whether you may route.

- Routing still works: capability classes are structural, not empirical.
- For accuracy, the device inherits **only** the device-agnostic baselines in
  `evidence/general/` — sleep tracking, HR sensor placement, steps and energy
  expenditure.
- **Do not transfer a device-specific number to a device it wasn't measured
  on.** One device's RMSSD offset or deep-sleep bias is not another's. Say
  what the general evidence supports and name the absence.

## ROUTING RULES

These are rule-based classifications by PRINCIPLE, not a fixed field list.
Platforms add data types over time, so classify anything new by which rule it
fits, not by memorising today's feature set.

**Route by capability class, not by brand.** A rule never says "the ring wins
sleep"; it says *the passively-worn continuous sensor governs passive
signals*, and each device declares which capability classes it has in
`devices.yaml`. **The RECORD carries the class, not the device** — an
auto-detected walk from a device that also does passive monitoring still
routes through Rule C, and a session recorded by that same device routes
through Rule B even if another device also declares `recorded_workout`.

Never name a device to pick a winner. Name the capability that produced the
record, then read which device that is.

### Rule A — `passive_247`: passive, continuous physiological monitoring

Worn 24/7, measured passively: sleep architecture, resting HR, HRV,
temperature, readiness/recovery scores, all-day stress, and any other passive
biometric a device measures now or adds later. **The device declaring
`passive_247` in `devices.yaml` is the governing source** for these signals.

- **Routing basis: `provisional` — and that must be VISIBLE, not smoothed
  over.** Two gaps the evidence does not close: (1) there is **no independent
  head-to-head** comparing a continuously worn passive device against a
  training watch for passive signals — "the passive sensor governs" is
  reasoned from device design, not measured; (2) current-generation sleep
  staging replication is thin and contested. When an answer leans on Rule A,
  say the routing is provisional.
- **Measurement confidence, per signal — these do not move with the routing
  basis:**
  - *Sleep/wake duration* — `high`. Trust it; total sleep time is well
    validated across brands.
  - *Sleep stages* — `low`. Do NOT present deep/REM minutes as fact.
    Documented systematic bias in both directions across generations. Trend
    only, and say so.
  - *HRV* — `moderate` as a trend against the user's own baseline;
    `unusable` as an absolute value or as a cross-device comparison. Ring-class
    devices have documented RMSSD underestimates (~15 ms vs ECG in the
    reference configuration's dossier), so the number is not comparable to a
    clinical figure or to another device. The correlation is good, so *change*
    is meaningful.
  - *Temperature deviation and all-day stress* — `unvalidated`. No citation at
    all. They ride the rule; say so when leaning on them.
- **Nutrition is explicitly NOT covered by this rule — see Rule D.** If a
  passive device ships meal tracking, it does not become the governing source
  for intake; at most it is a cross-check against Rule D.

### Rule B — `recorded_workout`: deliberately recorded sessions

A session the user deliberately started recording. **Rule B routes two
channels separately — this is the part that is easy to get wrong.** Never
merge them by averaging; report each with its own provenance and its own
confidence.

**`event` channel** — GPS, pace, distance, duration, power, cadence, training
load, VO2max, and any new workout-analysis metric.

- The record that actually captured the channel governs it. Usually only one
  overlapping record carries GPS or power at all, which makes the routing
  basis `structural`.
- If more than one overlapping record carries the channel, `devices.yaml →
  tiebreaks.recorded_workout` resolves it, and the basis becomes
  `user_preference` — say a preference decided it. If that tiebreak is unset,
  the observation is `unresolved`: report both with provenance.
- Measurement confidence: `high`. Nothing in the evidence challenges event
  data from a device built to record it.

**`heart_rate` channel** — **the best HR sensor class present in that window
governs, regardless of which device or app recorded the session.** Any
dedicated external monitor — chest strap *or* optical armband, any brand —
outranks wrist and ring. Routing basis `evidence_backed`; measurement
confidence is set by the sensor class and the session's intensity, not by the
rule. See HEART-RATE SENSOR CLASSES below.

**Do not assume the event winner also wins HR.** The sensor and the recorder
are different things, and the routed observation has a field for each.

### Rule C — `auto_detected`: incidental activity with no matching record

Walks, chores, general movement, steps, and any new auto-detected activity
type. **The detecting device is the governing source**, since nothing else has
a record of it.

- **Match on the absence of a competing *recorded* session, not on a source
  label.** Providers label detections variously (`autodetected`, `confirmed`,
  `manual`); a user-confirmed auto-detection is still Rule C. What
  disqualifies a record from Rule C is an overlapping recorded session
  (Rule B), not the value in its `source` field.
- **Routing basis: `structural`** — logically forced. Sole detector, no
  competing record, so no accuracy contest is needed and deduplication never
  fires across sources.
- **Measurement confidence: `moderate` for steps and active minutes.**
  Consumer step counts run ~9% low on average and free-living accuracy is
  materially worse than lab. Present daily totals as trends against the user's
  own baseline, not as exact counts.
- **Measurement confidence: `unusable` for energy expenditure.** This is the
  weakest number in the whole system — no consumer brand is accurate. It is
  fine to report a calorie figure when asked; it is not fine to reason from
  one, compare it across devices, or build a conclusion on it.

Rule C is the clearest illustration of why the two axes are separate: total
certainty about *which* device owns the bout buys nothing at all for the
*magnitude* it reports.

### Rule D — self-reported intake

Calories, protein, carbs, fat, individual food entries, meal timing: **the
user's own food log is the governing source.** Whatever logger they maintain
by hand — a phone app, a spreadsheet, `food-log.csv` in this repo. No sensor
outranks it.

**Rule D sits OUTSIDE the capability model.** It is self-reported, not sensed,
so none of the three capability classes covers it and no wearable evidence
bears on it. Its reliability grading is the `Source` column of the export
(barcode > quick/library/manual > photo), not a research dossier. See
NUTRITION DATA INTAKE below for the mechanics, which differ because there is
no server to query.

### When a record fits no rule

When a genuinely new data type appears that doesn't obviously fit A/B/C/D —
a new recovery metric, a new passive biometric, something that is neither
passive, recorded, detected nor self-reported — **don't guess silently.**

1. Name what it is, which source produced it, and which rule it most resembles.
2. Say what its capability class would have to be for each candidate rule.
3. Ask the user which rule it should follow.
4. Only then propose adding it to this file.

Until it is classified, treat it as `unresolved`: report it with its source
and say it is unrouted. Do not fold an unclassified metric into a total.

## CHANNELS — route channels, not records

Channel routing is a first-class principle of the framework, not a Rule B
detail. **A single real-world event may legitimately take different claims
from different sources**, because different sensors produced them and the
evidence about those sensors differs.

| Channel | Carries | Usual rule |
|---|---|---|
| `event` | GPS, pace, distance, duration, power, cadence, training load | B |
| `heart_rate` | In-workout heart rate, from whichever sensor class is present | B |
| `passive` | Sleep, resting HR, HRV, temperature, recovery scores | A |
| `incidental` | Steps, auto-detected bouts, general movement | C |
| `intake` | Self-reported food and drink | D |

Consequences that must be honoured:

- **One record can produce several routed observations.** A recorded session
  yields at least an `event` observation and a `heart_rate` observation. They
  share a window and carry separate sources, separate rules and separate
  confidence.
- **A losing record on one channel may still govern another.** When two
  devices record the same session, neither "wins the record" — each channel is
  routed, and both appear in the other's provenance.
- **Never flatten channels into a single winner**, and never average across
  them.
- Add a channel only when a real source produces a claim an existing channel
  cannot carry without misstating its provenance. Do not invent speculative
  channels.

## HEART-RATE SENSOR CLASSES (Rule B, `heart_rate` channel)

In-workout HR is the channel where the recording device does **not**
automatically govern. Route it by **sensor class and placement — never by
brand, and never by which app started the session.**

| Class | What it is | Measurement confidence |
|---|---|---|
| `external_hr_monitor` | A dedicated HR device worn away from the wrist. Two subtypes below. | **High** |
| ├ `ecg_chest_strap` | Electrical, reads the ECG signal directly — any BLE HR Service strap, any brand | **Highest.** rc=0.98–0.99 vs ECG; used as the *criterion* in other studies |
| └ `optical_armband` | Optical PPG at the upper arm or forearm | **High.** MAE 1.43 bpm, MAPE 1.35%, CCC 1.00 (upper arm); ICC 0.99 across arm sites |
| `wrist_optical` | Watch PPG at the wrist | **Low during exercise.** MAE 6.41 bpm, CCC 0.92 head-to-head; rc≈0.52 on one tested model; degrades as intensity rises |
| `ring_ppg` | Ring PPG | **Unvalidated during exercise — no study exists.** Ring HR/HRV evidence is nocturnal/at-rest only |
| `other_ble` | Earbuds, gym equipment, anything else broadcasting BLE HR | **Unvalidated — uncited.** Treat as undeclared |

**Placement, not brand, is what the evidence separates.** Optical at the arm
is a different measurement problem from optical at the wrist: less motion
artifact, better optical coupling. An armband is *not* a downgrade from a
chest strap for routing purposes — in a direct head-to-head against an ECG
criterion, the armband beat the wrist by roughly 4.5× on mean absolute error.

**Routing:**

1. If any record overlapping the session has an `external_hr_monitor` (either
   subtype), **its HR governs the channel** — even if a different device
   governs the event channel. A monitor paired to a phone or ring app
   outranks an unmonitored watch for HR, and the watch still owns pace, GPS
   and power for the same session.
2. If both subtypes are present for one session (rare), prefer
   `ecg_chest_strap` — it is the reference standard the armband is validated
   *against*.
3. If no external monitor was present, keep the **recording device's** HR (it
   is time-aligned and purpose-recorded), and **scale measurement confidence
   to the session's intensity.** The wrist-optical penalty is not a constant:
   all devices were accurate **at rest**, with accuracy falling *as intensity
   rises*. A blanket low-confidence flag overstates the problem for
   near-resting sessions and understates the intensity dependence.
   - **Near-resting** (yoga, stretching, pilates, gentle walking — session avg
     HR at or near the user's resting baseline): wrist optical is inside the
     regime where it *was* validated as accurate. Confidence `moderate`.
     Report normally; note the absence of a monitor once, without alarm.
   - **Moderate to high intensity**: confidence `low`. Say it in words — do
     not report a bare number.
   - **Intervals or rapid HR change**: `low`, and the lowest of the non-water
     cases. Optical sensors lag transitions; averages may look reasonable
     while the peaks and recoveries are wrong.
   - **Swimming and other in-water activity**: `unusable` from **every**
     sensor class. Water defeats wrist optical, and BLE/ANT+ does not transmit
     through water, so a strap cannot help unless it records onboard. Do not
     compare a swim HR against another session's.
4. **`ring_ppg` never takes over from `wrist_optical`.** No external monitor
   does not mean the ring governs; it means *nobody* has trustworthy
   in-workout HR. Swapping in an unvalidated number because the
   validated-bad one looks bad is a downgrade disguised as an upgrade —
   `unvalidated` is not better than `low`, it is less knowable.

   Note the asymmetry this creates, and use it: for **near-resting** sessions
   both sensors are inside their validated regimes (wrist optical is accurate
   at rest; ring HR has a small measured bias overnight). So for yoga or
   stretching the two devices should broadly **agree**, which makes them a
   genuine cross-check. **A large disagreement on a low-intensity session is a
   signal worth reporting**, not something to resolve by picking a winner. At
   higher intensity the comparison loses its footing — one sensor is
   known-bad and the other unstudied — so a disagreement there says little.
5. **Never average across sensor classes.**

**Two caveats that survive the good numbers:** optical armbands can lag during
rapid HR transitions (intervals, sprint starts), and they are
placement-sensitive — a loose or mis-sited band degrades badly. For interval
work specifically, a chest strap remains preferable.

### Where monitor use is declared

**No API reports which HR sensor fed a session.** A recorder field such as
`device_manufacturer` names the *recorder*, not the sensor. Running dynamics
are not a proxy either — some watches generate them at the wrist.

So it is declared in **`devices.yaml`**, under `external_hr_monitors`
(`owned` and `worn_for`). Read it, don't guess.

- Activity types under `worn_for.unknown`, or not listed at all, are **treated
  as unmonitored for confidence purposes** — grade the HR by the recording
  device's own sensor class rather than silently assuming a monitor was worn.
- When an unlisted activity type actually matters to a conclusion, **ask**
  instead of inferring. If the answer would change either way, the observation
  is `withheld` until the user says.
- If `devices.yaml` has no `external_hr_monitors` block, say monitor status is
  undeclared and apply the no-monitor branch above.

## MULTIPLE DEVICES, SAME CLASS

Two devices can declare the same capability class (two rings, a watch and a
band, a strap and a watch both recording).

1. **`recorded_workout` on both** → not a conflict; it is one event. Merge by
   channel per Rule B and the DEDUPLICATION rules below.
2. **`passive_247` on both** (e.g. a ring and a 24/7 watch) → use
   `tiebreaks.passive_247` in `devices.yaml`. Routing basis becomes
   `user_preference`. If it is unset, **the observation is `unresolved`:
   report both with provenance.** Do not pick silently, and never average.
3. **`auto_detected` on both** → whichever detected the bout owns it (Rule C).
   If both detected the same bout, deduplicate; do not sum.

**Tiebreaks are user preference, not evidence** — there is no study
establishing that one 24/7 wearable beats another for passive signals. A
tiebreak resolves *routing* deterministically and improves *measurement
confidence* by exactly nothing. **Say so when a tiebreak decided an answer**,
and keep the losing value in the observation's `competing` list so the spread
stays visible.

## SINGLE-DEVICE SETUPS

One device is a valid configuration. Rules A/B/C still apply — they just all
resolve to the same device, and the deduplication step is a no-op *across*
sources (still run the within-source duplicate check).

Nothing is cross-validated, so **confidence is lower, not higher**: there is
no second record to catch an anomaly, and no disagreement to surface. Say that
when it matters. Do not present a single-source number as more certain because
nothing contradicted it.

## DEDUPLICATION (critical — do this before any analysis)

- Before combining or summing activity data, check for time-overlapping
  events — across sources AND within each source. Multiple providers can emit
  recorded sessions, so "one device records, the other detects" is not a safe
  assumption in any configuration.
- **Use a ±12 minute overlap buffer** throughout — the midpoint of the 10–15
  min lag between a real event and a passive device's auto-detection of it.
- **Case 1 — recorded vs auto-detected** (the common one): if a recorded
  activity and an auto-detected session overlap, treat them as the SAME
  real-world event. Keep the recorded version's metrics and ABSORB the
  auto-detected entry — record it in `merged_from` with disposition
  `absorbed`, then drop it from totals.
- **Case 2 — recorded vs recorded**: two recorded sessions that overlap are
  still ONE event. Do not pick a single winner for the whole record — **merge
  by channel**: `event` to the recorder that captured it (or the
  `tiebreaks.recorded_workout` preference when both did), `heart_rate` to
  whichever carries an `external_hr_monitor`. Record `merged_from` on both
  observations with disposition `superseded_by_channel`, and say explicitly
  which channel came from which device.
- **Case 3 — duplicates within ONE source**: a single provider can emit
  near-identical records for one event (observed in the reference
  configuration: one provider returned the same walking bout three times in a
  day, with calories 56 / 56 / 55.746). Deduplicate *within* each source
  before comparing across sources, or daily totals inflate. Match on
  overlapping time window and activity type; keep one, record the collapse
  with disposition `duplicate_collapsed`. **Do not treat near-identical
  calorie values as evidence of separate events** — the small numeric
  differences are the tell, not a counter-argument.
- **Overlap is necessary but not sufficient.** Two genuinely separate bouts
  can fall inside the buffer — a warm-up walk and the run that follows it, two
  lifts either side of a break. Before collapsing, check that activity type
  and duration are consistent with one event. If they are not, keep both and
  say why you kept them. Over-merging is as wrong as double-counting, and
  harder to notice.
- Only count an auto-detected session as genuine incidental activity if it has
  no corresponding recorded activity in that time window.
- When calculating daily totals (calories, active time, steps), be explicit
  about which source contributed which portion, so the user can sanity-check
  the math if a total looks off.

## PRESERVING DISAGREEMENT

The framework's job is to route, not to manufacture agreement. Sources
disagreeing is information; hiding it is the failure mode this whole model
exists to prevent.

- **Never average conflicting sensors.** Averaging invents a value neither
  device measured, which is worse than either of them.
- **Select a source only when a rule or an explicit tiebreak allows it.**
  Absent both, the observation is `unresolved` and both values are reported
  with their provenance.
- **Preserve what lost.** An absorbed duplicate goes in `merged_from`; an
  unresolved competitor goes in `competing`. Nothing is dropped silently.
- **"Selected" is not "correct."** A selected source is the one a rule
  designated, not the one shown to be right. Say "routed from X under Rule Y",
  not "X is correct". Where two devices disagree materially and the rule that
  picked one is `provisional` or `user_preference`, the disagreement is part
  of the answer.
- **A large disagreement inside both sensors' validated regimes is a finding**
  — surface it rather than resolving it by preference.

If the user asks you to just average two sensors: say plainly why that
produces a number neither device measured, report both values with their
provenance and confidence, and offer the comparison they probably want — which
source is routed for this metric, how far apart the two are, and what the
spread means given each one's error. If they reaffirm the request after that,
it is their call: give the mean, label it as user-requested, state that it is
not a measurement, and keep both source values next to it. Never let a
requested average become the routed value or feed a downstream conclusion.

## THE ROUTED OBSERVATION (canonical provenance)

Every number you route is represented internally as a **routed observation**:
one metric, one channel, one time window. This is a working contract, not a
storage format — build them while analysing, keep them in context, surface
what is material. The full schema and worked examples are in
the plugin skill's `references/routed-observation.md`
([online](https://github.com/drleahzou/MetricBraid/blob/main/spec/routed-observation.md), with the
[JSON Schema](https://github.com/drleahzou/MetricBraid/blob/main/spec/routed-observation.schema.json)).

| Field | Holds |
|---|---|
| `metric`, `value`, `unit`, `window` | What was measured, over what span. `value` is null unless `routing_status` is `routed` |
| `channel` | `event` · `heart_rate` · `passive` · `incidental` · `intake` |
| `routing_status` | `routed` · `unresolved` · `withheld` |
| `selected_source` | `device` (id from `devices.yaml`), `capability_class` of *this record*, `sensor_class`, `record_id` |
| `routing` | `rule` (A/B/C/D), `basis`, `decided_by` — why this source |
| `measurement` | `confidence`, `evidence` (dossier paths), `caveats` — what the number is worth |
| `merged_from` | Records absorbed for the same event, with disposition |
| `competing` | Disagreeing values nothing resolved |
| `must_disclose` | Statements that have to reach the user when this observation is material |

**The recorder and the sensor are separate fields on purpose.** A strap paired
to a ring's app is `device:` the ring's record, `sensor_class:
ecg_chest_strap`. Collapsing them is how brand creeps back into routing.

A worked example — one recorded run with an overlapping auto-detection and a
declared chest strap produces two observations:

```
event        distance_m 8412 m   routed  ← recorder, Rule B, basis structural,
                                            measurement high
                                            merged_from: auto-detected bout (absorbed)
heart_rate   avg_hr 152 bpm      routed  ← same record, sensor ecg_chest_strap,
                                            Rule B, basis evidence_backed,
                                            measurement high
```

Same event, same window, two sources of authority, no averaging, and the
absorbed record still visible. See [`spec/examples/`](https://github.com/drleahzou/MetricBraid/blob/main/spec/examples/) for the full JSON, plus a
`user_preference` tiebreak case, an `unresolved` conflict, and a `withheld`
observation.

### What must be surfaced

Provenance is carried for everything; it is *reported* when material — when it
would change what the user does, how much they trust a number, or whether a
comparison is believable at all. **Always surface:**

- every entry in `must_disclose`
- a `routing.basis` of `provisional`, `user_preference` or `unresolved`
- a `measurement.confidence` of `low`, `unvalidated` or `unusable`
- any `routing_status` other than `routed`
- that a merge happened, whenever a total or a count is reported

A bare number is only appropriate when the basis is `structural` or
`evidence_backed`, confidence is `high`, and nothing was merged. If you cannot
answer "which source produced this, under which rule, and how good is the
number", you cannot defend it — say so instead of reporting it.

## CONFIDENCE: TWO AXES, NEVER COLLAPSED

Two different questions, graded separately on every observation:

- **`routing.basis`** — how firmly do we know *which source should own this*?
  `structural` (forced by the shape of the data) · `evidence_backed` (a cited
  dossier establishes the ordering) · `provisional` (reasoned, not measured, with
  a named gap) · `user_preference` (a tiebreak decided it) · `unresolved`
  (nothing did).
- **`measurement.confidence`** — how much is *the number itself* worth?
  `high` · `moderate` · `low` · `unvalidated` · `unusable`.

They move independently, and the awkward combinations are the common ones:

| Case | Basis | Measurement |
|---|---|---|
| Solo-detected walk's step count | `structural` — nothing else saw it | `moderate` — ~9% systematic undercount |
| The same walk's calorie figure | `structural` | `unusable` — no brand is accurate |
| HR with a declared chest strap | `evidence_backed` | `high` |
| HR from a wrist sensor at effort | `evidence_backed` — the hierarchy is cited | `low` — the same citation says so |
| Sleep duration under Rule A | `provisional` — the ordering is reasoned | `high` — duration is well validated |
| Passive signal decided by a tiebreak | `user_preference` | Unchanged by the tiebreak |
| Two passive devices, no tiebreak | `unresolved` | Ungraded — report both |

**`unvalidated` is not `low`.** `low` means studied and found poor in this
regime, so you can say how wrong it is likely to be. `unvalidated` means
nobody has looked, which licenses no claim in either direction. This
distinction is what stops an unstudied sensor being promoted over a
known-imperfect one.

Never describe a measurement as reliable because its routing was certain, or a
routing as sound because the measurement was well studied.

## KNOWN DATA-SOURCE DEFECTS

**Check `devices.yaml` → `known_defects` before trusting any tool's output.**
These are bugs that return plausible-looking data rather than an error, so
they cannot be caught by checking for failures.

- A metric covered by an open defect is `withheld`, not routed. Say the data
  is unavailable and why — do not report what the tool returned.
- Say what the defect makes *impossible*, not just what it makes unreliable.
  If a defect blocks a cross-device comparison, the comparison is off the
  table, not merely caveated.
- **Do not quietly route around a defect.** Substituting another source
  without saying so turns a known gap into an invisible one.

When you hit a new defect: verify it (same request, different inputs, look for
impossible invariance), tell the user, add it to `devices.yaml →
known_defects` with what you observed, and note it in
`evidence/CHANGELOG.md`. A silently wrong number is worse than a missing one.

## EVIDENCE STATUS AND DISCIPLINE

Verdicts decay — firmware ships, generations change, a 2019 study describes a
device nobody wears now. The rules above are only trustworthy if their
evidence is kept honest. Dossiers ship with the plugin skill as
`references/` (`evidence/` in the repo), in two tiers:

- **`evidence/general/`** — device-agnostic, multi-brand or mechanism-based.
  Every setup inherits these regardless of hardware: consumer sleep tracking,
  HR sensor placement, steps and energy expenditure.
- **`evidence/devices/`** — per-device specifics. These do **not** transfer
  between devices. A number measured on one device says nothing about another.

Where a device dossier and a general dossier disagree, the device dossier is
more specific and wins **for that device only**. A device with no dossier
inherits `general/` and nothing more.

- **Source-quality bar, in order:** peer-reviewed validation studies (vs
  polysomnography for sleep, vs ECG for HR/HRV) > independent testers with
  published reference-device methodology > **never** vendor marketing, spec
  sheets, press coverage, or uncited recollection.
- **Never cite a study from memory.** If a claim about device accuracy matters
  to an answer, it comes from a dossier in `evidence/` or it gets read against
  the primary source first. This is where health claims quietly fail.
- **A dossier grades measurements, not routing.** Adding evidence for a device
  never promotes it over another device; capability classes decide that.
- **A new finding is never an automatic rule change.** If something relevant
  surfaces (new validation study, new firmware, a device change), raise it,
  record it, and only then propose a rule edit — and log the edit in
  `evidence/CHANGELOG.md`, including reviews that conclude "no change."

## NUTRITION DATA INTAKE (Rule D mechanics)

Unlike the sensor integrations, the intake source has **no MCP server**. It
cannot be queried. This changes the failure mode, so handle it explicitly:

- Food data arrives only when the user pastes it in or drops an export into
  the repo. `food-log.example.csv` shows the expected header; copy it to
  `food-log.csv` (gitignored) and fill it in.
- **If asked about intake and nothing has been provided this session, say so
  and ask for it.** Do not answer from an earlier session's numbers as if they
  were current, and never infer intake from sensor-estimated calorie
  *expenditure* — burn is not intake, and expenditure is `unusable` anyway.
- Weight entries by how they were captured, which the export's `Source` column
  records:
  - `barcode` — copied off a physical Nutrition Facts panel. Highest
    confidence.
  - `quick` / `library` / `manual` — reference values or the user's own saved
    figures. Good, but portion size is still estimated.
  - `photo` — hand-portion estimate. **Treat as a rough bracket, not a
    measurement.** The photo is usually retained in the logging app, so if a
    conclusion depends on one of these, ask for the image and re-estimate
    rather than trusting the logged number.
- A nutrition endpoint on a *sensor* platform is a **mirror, not a source**.
  It is only populated if a pasted batch was deliberately pushed there. If it
  ever disagrees with the user's own log, the user's log governs and the
  mirror is stale.
- Say which day's data you actually have. Partial logging is normal — a day
  with 900 kcal recorded usually means they stopped logging, not that they ate
  900 kcal. Flag suspected under-logging instead of treating the total as
  fact.

## USE EVERYTHING AVAILABLE — DON'T PRE-FILTER

- Before analysis, enumerate the full list of tools and resources currently
  exposed by every configured MCP server — not just the metrics named in this
  file. Pull from any that are relevant to the question, including newer or
  less obvious ones (SpO2, cardiovascular age, respiration rate, resilience,
  tags, cycle tracking, workouts — whatever currently exists).
- Treat this file as a set of ROUTING RULES for when sources conflict or
  overlap, not a whitelist of what you're allowed to look at. If a data type
  isn't mentioned here but is available and relevant, use it — and if it
  doesn't fit a rule, follow "When a record fits no rule".

## ANALYSIS PHILOSOPHY

- The goal is understanding the INTERPLAY between systems, not just reporting
  numbers. When asked about any single metric, proactively note relevant
  cross-domain connections if they exist in the data — how a hard recorded
  session affected next-day passive HRV/readiness, how sleep debt correlates
  with training-load tolerance, how incidental movement affects recovery on
  top of deliberate training, how stress trends precede dips in performance.
- Always cite which source a number came from when it isn't obvious.
- Flag anomalies or notable pattern breaks, not just averages.
- Avoid generic textbook fitness advice — ground every observation in the
  user's actual numbers pulled from the tools, not assumptions.
- When data is missing or a tool call returns nulls, say so explicitly rather
  than guessing or filling gaps with typical values.

## SUBJECTIVE / QUALITATIVE DATA

Workout notes, perceived effort, "feel" ratings, any free-text the user
enters.

- Treat these as a SIGNAL to investigate, not a fact to simply repeat back.
  They carry information the sensors can't capture — motivation, pain, life
  stress, illness onset — but they're also self-reported and subject to bias,
  so weigh them against the quantitative data rather than accepting or
  dismissing them outright.
- When a note and the sensor data agree, that's confirmatory — say so, it
  strengthens confidence in the read.
- When they DISAGREE (the note says "felt easy" but HR was elevated
  throughout, or "rough session" but metrics look unremarkable), flag the
  mismatch explicitly and propose plausible explanations (heat, dehydration,
  incomplete recovery, illness incubating, poor sleep the prior night, life
  stress not captured by any device, or a sensor artifact) rather than
  silently picking one source as "correct."
- Use qualitative notes to help explain WHY a quantitative anomaly happened,
  and quantitative data to sanity-check WHETHER a qualitative impression is
  backed by physiology. Neither overrides the other by default — they're
  cross-validation, not a hierarchy.

## ANALYTICAL STANDARDS

Apply to every interpretive claim, not just formal "analysis" requests — this
governs HOW to reason about the data, not just which data to use.

- **Correlation vs. causation**: describe observed relationships as
  "associated with" or "coincided with," not "caused by," unless there's an
  established physiological mechanism (intense training suppressing next-day
  HRV is fine to state causally; "your stress score is high because you had
  coffee at 3pm" is a guess unless the data supports it).
- **Confounders**: before attributing a change in one metric to another,
  consider and rule out other explanations where possible — illness, alcohol,
  travel/jet lag, heat, altitude, medication or supplement changes, caffeine
  timing, hormonal cycle phase (if tracked), poor sleep environment. If you
  don't have data to rule these out, say the confounder is unaddressed rather
  than ignoring it.
- **Time lag matters**: recovery and readiness metrics often reflect stress
  from 1–2 days prior, not the same day. Check multiple lag windows
  (same-day, next-day, +2 days) rather than assuming same-day correlation is
  the right one.
- **Personal baseline over population norms**: compare the user's metrics to
  THEIR OWN rolling historical average and typical variability range, not
  generic "normal" ranges. Default parameters: **30-day rolling window, at
  least 7 days of data before calling anything anomalous, 2σ threshold.** This
  isn't a stylistic preference — given documented absolute biases such as a
  ~15 ms RMSSD underestimate and a ~9% step underestimate, **their own history
  is the only valid reference frame**; a population norm compared against a
  biased absolute number is meaningless.
- **Sample size honesty**: don't generalize a pattern from one or two
  occurrences. If something looks like a trend but rests on limited data
  points, say so explicitly, describe it as a hypothesis rather than a
  conclusion, and suggest what additional data would confirm or refute it.
- **Consider alternative explanations**: before settling on the most likely
  interpretation of a pattern, briefly note at least one plausible
  alternative, especially when the stakes are high ("you're overtraining" vs.
  "you're getting sick" vs. "this is normal week-to-week variability").
- **Metric limitations**: distinguish raw physiological measurements (HR, HRV
  in ms, sleep stage durations) from proprietary composite scores (readiness,
  training status, body battery). Composite scores are useful summaries but
  can obscure what's actually driving a change — when relevant, look at the
  underlying contributors rather than just reporting the score.

## STAY CURRENT WITH DEVICE UPDATES

- At the start of any new session (or if the user asks "what's new"), briefly
  check whether the configured MCP servers expose tools, resources, or data
  fields that aren't reflected in this file's known categories.
- If you notice something new — a new metric, a new tool, a new data category
  — tell the user proactively: name what's new, which source it came from, and
  suggest which rule it should fall under.
- Don't silently start or stop using a data type without mentioning it once.
  After the user confirms how to classify it, update this file so the rule
  persists.
- This check should be lightweight — a quick scan of available tools, not a
  deep audit every time.

## BUNDLED INTEGRATIONS AND AUTHENTICATION

The routing model above is hardware-agnostic. The **plumbing** is not: this
repo currently bundles MCP servers for two providers, configured in
`.mcp.json`. Which capability classes they provide is declared in
`devices.yaml`, not here.

- **Garmin Connect** (`garmin` server — Taxuspt/garmin_mcp, 110+ tools):
  recorded activities, training load, VO2max, HRV, resting HR, sleep, stress,
  Body Battery, workout detail, and more.
- **Oura Ring** (`oura` server — mitchhankins01/oura-ring-mcp, ~27 tools):
  daily sleep, readiness, HRV, resting HR, activity, auto-detected sessions,
  temperature, stress, SpO2, resilience, cardiovascular age, tags, and more.

Any other source works the same way once its records reach the session: add a
community MCP server to `.mcp.json` and declare the device in `devices.yaml`,
or paste exports in. The rules don't care where records come from — Rule D has
always worked with no server at all.

**Garmin auth**: tokens live in `~/.garminconnect/` (created by running
`garmin-mcp-auth` interactively — supports MFA; tokens last ~6 months).
Alternatively `GARMIN_EMAIL`/`GARMIN_PASSWORD` env vars work
non-interactively for accounts without MFA. If the garmin server exits at
startup, authentication is the first thing to check. See `SETUP.md`.

**Oura auth**: requires the `OURA_ACCESS_TOKEN` env var, which must be an
**OAuth2 access token**.

- **Personal Access Tokens (PATs) are dead. Oura deprecated them in Dec 2025 —
  newly generated PATs return 401 and DO NOT WORK.** The PAT page still exists
  and still hands out tokens, which is why this trap catches people. If a PAT
  is what's in the env var, no amount of regenerating will fix it. Tokens
  minted before the deprecation still work but cannot be replaced once
  revoked.
- **Never advise regenerating or deleting a token as a first move.** If a
  pre-deprecation PAT is still working, deleting it is irreversible — there is
  no way to mint a replacement PAT. Migrate to OAuth2 instead.
- Get an OAuth2 token by registering a personal application at
  https://cloud.ouraring.com/applications with a localhost redirect URI, then
  completing the authorization code flow. OAuth access tokens are sent as the
  same `Bearer` token against the v2 API, but they **expire in ~24h**, so a
  refresh step is required for unattended use. See `SETUP.md`.
- **On any Oura 401, debug in this order — never jump to "get a new token":**
  (a) confirm the env var is actually visible to the MCP server process, not
  just to your interactive shell; (b) curl the v2 API and print ONLY the HTTP
  status, never the token; (c) check whether the token is a PAT (dead) or
  OAuth2 (refreshable); (d) if OAuth2 and expired, refresh it. Remember the
  MCP server captures its environment at session start — restart the session
  after any env change.

Never commit credentials or tokens to this repository. `.gitignore` blocks
`.env*`, token directories, and `.claude/settings.local.json`.

## SAFETY BOUNDARY

These are consumer devices and this is tooling for personal data analysis.
**Nothing here is a diagnostic instrument, and none of this is medical
advice.** Routing a number carefully does not make it clinical-grade; most of
what the framework does is establish how *little* some numbers support.

When evidence is absent, stale, provisional or device-specific, say so
explicitly rather than rounding up to confidence. If a question is really a
medical one — a symptom, a diagnosis, a medication decision — say that the
data can describe a pattern but cannot answer it, and that a clinician can.
