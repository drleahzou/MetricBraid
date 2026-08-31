---
name: health-data-routing
description: Route and reconcile personal sensor data when several devices produce overlapping or conflicting records of the same events. Use whenever the user asks about their sleep, HRV, resting heart rate, readiness, recovery, training load, VO2max, steps, workouts, stress, body battery, temperature, SpO2, or nutrition — and especially when combining, totaling, or comparing data across devices, or when asked "how am I doing", "am I recovered", "am I overtraining", or "am I getting sick". Also use when a daily total needs computing from more than one source, when two devices disagree, or when the user asks how much to trust a number.
---

# Personal sensor evidence routing

When several devices observe the same body, they produce overlapping,
disagreeing claims about the same physical events. This skill decides which
source governs which claim, prevents double-counting, and constrains how
confidently conclusions may be stated.

```
candidate observations → routing / arbitration → confidence → provenance → answer
```

**If a configured source fails to connect, say so before analysing. Never
substitute assumptions for missing tool output**, and never let a silently
absent source hand an uncontested win to whatever did respond.

## First: read `devices.yaml`

**This skill names no hardware.** Which device provides which capability is
declared in the project's `devices.yaml` — **read it before routing** and never
infer hardware from which MCP servers happen to respond.

- Missing file, or a device not listed → **say so and ask.** Do not guess.
- Listing a device declares **capabilities only**. It confers no accuracy
  claim; accuracy comes only from a dossier in `references/`.
- **Devices with no dossier are normal.** Routing still works (capability
  classes are structural). For accuracy they inherit only the device-agnostic
  baselines in `references/general/`. **Never transfer a device-specific
  number to a device it wasn't measured on** — say the number is unavailable
  for that device instead. Adding a dossier never promotes a device in the
  routing; it only changes what may be said about its numbers.

**Two devices declaring the same class:** both `recorded_workout` → one event,
merge by channel. Both `passive_247` → use `tiebreaks` in `devices.yaml`; if
unset, report both with provenance and say the conflict is unresolved. Never
average. A tiebreak is user preference, not evidence — say so when one decided
the answer.

**A single device is valid.** Rules still apply, all resolving to one device.
Confidence goes *down*, not up: nothing cross-validates it.

## Two confidences, never collapsed

Grade every number on **two independent axes**. Conflating them is the failure
this skill exists to prevent — it makes a routing decision sound like a
validated measurement.

- **Routing basis** — how firmly we know *which source should own this*.
  `structural` (forced by the shape of the data) · `evidence_backed` (a cited
  dossier establishes the ordering) · `provisional` (reasoned, not measured,
  with a named gap) · `user_preference` (a tiebreak decided it) · `unresolved`
  (nothing did).
- **Measurement confidence** — how much *the number itself* is worth.
  `high` · `moderate` · `low` · `unvalidated` · `unusable`.

The awkward combinations are the common ones: a solo-detected walk is
`structural` + `unusable` for calories; sleep duration under Rule A is
`provisional` + `high`; wrist HR at effort is `evidence_backed` + `low`.

**`unvalidated` is not `low`.** `low` means studied and found poor in this
regime, so you can say how wrong it probably is. `unvalidated` means nobody
looked, which licenses no claim in either direction.

## Route by capability class, not by brand

A rule never says "the ring wins sleep." It says *the passively-worn
continuous sensor governs passive signals*. Each device declares which
capability classes it has in `devices.yaml`:

- `passive_247` — worn continuously, measures passively → **Rule A**
- `recorded_workout` — sessions deliberately started → **Rule B**
- `auto_detected` — activity the device notices on its own → **Rule C**

**The RECORD carries the class, not the device.** An auto-detected walk from a
device that also does passive monitoring routes through Rule C. A session
recorded by that same device routes through Rule B even if another device also
declares `recorded_workout`. Never name a device to pick a winner — name the
capability that produced the record, then read which device that is.

Assume nothing about which device does what. A ring may record sessions; a
watch may monitor 24/7. "One records, the other detects" is not a safe
assumption in any configuration.

These are classifications by principle, not a fixed field list. Platforms add
data types over time; classify anything new by which rule it fits.

## Route channels, not records

**A single real-world event may legitimately take different claims from
different sources**, because different sensors produced them.

| Channel | Carries | Usual rule |
|---|---|---|
| `event` | GPS, pace, distance, duration, power, cadence, training load | B |
| `heart_rate` | In-workout HR, from whichever sensor class is present | B |
| `passive` | Sleep, resting HR, HRV, temperature, recovery scores | A |
| `incidental` | Steps, auto-detected bouts, general movement | C |
| `intake` | Self-reported food and drink | D |

One record produces one observation per channel. A losing record on one
channel may still govern another, and appears in the other's provenance.
Never flatten channels into a single winner, and never average across them.

## The rules

### Rule A — `passive_247`: continuous passive physiological monitoring

Sleep architecture, resting HR, HRV, temperature, readiness/recovery scores,
stress, and any other passive biometric. **The device declaring `passive_247`
is the governing source.**

**Routing basis: `provisional` — say so out loud when leaning on it.** Two
gaps the evidence does not close: (1) there is no independent head-to-head
comparing a 24/7 passive device against a training watch for passive signals —
that ordering is reasoned from device design, not measured; (2)
current-generation staging replication is thin and contested.

Measurement confidence, per signal:
- **Sleep/wake duration** — `high`. Trust it; total sleep time is well
  validated.
- **Sleep stages** — `low`. Do NOT present deep/REM minutes as fact.
  Documented systematic bias in both directions across generations. **Trend
  only.**
- **HRV** — `moderate` as a trend against the user's own baseline; `unusable`
  as an absolute value or across devices. Ring-class devices have documented
  RMSSD underestimates (~15 ms vs ECG in the reference dossier), so the number
  is not comparable to a clinical figure or another device. The *correlation*
  is good, so *change* is meaningful.
- **Temperature deviation and all-day stress** — `unvalidated`. No citation at
  all. Say so when leaning on them.

Nutrition is explicitly **not** covered by Rule A — see Rule D.

### Rule B — `recorded_workout`: deliberately recorded sessions

Rule B routes **two channels separately** — this is the part that is easy to
get wrong.

**`event` channel** (GPS, pace, distance, duration, power, cadence, training
load, VO2max): the record that actually captured the channel governs it —
usually the only one that carries it at all, which makes the basis
`structural`. If more than one overlapping record has it, `tiebreaks.recorded_workout`
resolves it and the basis becomes `user_preference`; if that is unset, report
both. Measurement confidence `high`.

**`heart_rate` channel**: the **best HR sensor class present wins, regardless
of which device or app recorded the session.** Do not assume the event winner
also wins HR. Basis `evidence_backed`; measurement confidence set by sensor
class and intensity.

Route by sensor class **and placement** — never by brand, never by which app
recorded the session.

| Class | What it is | Measurement confidence |
|---|---|---|
| `ecg_chest_strap` | Any chest strap, any brand (any BLE HR Service strap) | **Highest** — rc=0.98–0.99 vs ECG; used as the *criterion* in other studies |
| `optical_armband` | Optical PPG at upper arm/forearm | **High** — MAE 1.43 bpm, CCC 1.00 (upper arm); ICC 0.99 across arm sites |
| `wrist_optical` | Watch PPG at the wrist | **Low during exercise** — MAE 6.41 bpm, CCC 0.92 head-to-head; rc≈0.52 on one tested model; worsens as intensity rises |
| `ring_ppg` | Ring PPG | **Unvalidated during exercise** — no study exists; ring evidence is nocturnal/at-rest only |
| `other_ble` | Earbuds, gym equipment, any other BLE HR broadcaster | **Unvalidated, uncited** — treat as undeclared |

The first two together are the routing class **`external_hr_monitor`**.
Placement is the variable, not brand or price: optical at the arm is a
different accuracy regime from optical at the wrist (less motion artifact,
better optical coupling), and beat the wrist ~4.5× on MAE in a same-brand,
same-protocol head-to-head.

Routing:
1. If any overlapping record has an `external_hr_monitor` (**either**
   subtype), **its HR governs the channel** even if another device won the
   event channel. A monitor paired to a phone or ring app outranks an
   unmonitored watch for HR, while the watch still owns pace/GPS/power for
   that same session.
2. If both subtypes are present (rare), prefer `ecg_chest_strap` — it is the
   reference standard the armband is validated against.
3. If no external monitor, keep the **recording device's** HR and **scale
   measurement confidence to intensity** — the wrist-optical penalty is not
   constant. Both ECG studies found all devices accurate *at rest*, with
   accuracy falling as intensity rises; rc≈0.52 is an *exercise* figure.
   - *Near-resting* (yoga, stretching, pilates, gentle walking): `moderate` —
     wrist optical is inside its validated-good regime. Report normally; note
     the missing monitor once, without alarm.
   - *Moderate/high intensity*: `low`. Say it in words, not as a bare number.
   - *Intervals*: `low`, and the lowest non-water case — optical lags
     transitions, so the average can look fine while peaks and recoveries are
     wrong.
   - *Swimming / in-water*: `unusable` from **every** sensor class. Water
     defeats wrist optical, and BLE/ANT+ does not transmit through water, so a
     strap cannot help unless it records onboard. Never compare a swim HR
     against another session's.
4. **`ring_ppg` never takes over from `wrist_optical`.** No monitor does not
   mean the ring wins — it means nobody has trustworthy in-workout HR.
   Swapping a measured-poor number for an unmeasured one is a downgrade
   disguised as an upgrade.

   The asymmetry is usable: at near-resting intensity both sensors are inside
   validated regimes, so they should broadly agree, which makes a
   low-intensity session a genuine cross-check. **A large disagreement there
   is a signal worth reporting**, not something to resolve by picking a
   winner. At higher intensity the comparison loses its footing.
5. **Never average across sensor classes.**

Armbands lag on rapid HR transitions and are placement-sensitive, so a chest
strap stays preferable for interval work.

**Monitor use is not detectable from the APIs.** A recorder field such as
`device_manufacturer` names the *recorder*, not the sensor, and running
dynamics are not a proxy on watches that generate them at the wrist. It must
be **declared in `devices.yaml` under `external_hr_monitors`**. If undeclared
for that activity type, say so and treat it as unmonitored for confidence — do
not infer. If it would change the conclusion, ask.

### Rule C — `auto_detected`: incidental activity with no matching record

Walks, chores, general movement, steps. **The detecting device is the
governing source**, since nothing else has a record of it.

**Match on the absence of a competing recorded session, not on a source
label** — providers label detections variously (`autodetected`, `confirmed`,
`manual`), and a user-confirmed detection is still Rule C.

**Routing basis: `structural`** — logically forced: sole detector, no
competing record. **Measurement confidence: `moderate` for steps and active
minutes** (consumer step counts run ~9% low, free-living materially worse than
lab; present totals as trends against the user's own baseline, not exact
counts).

**Energy expenditure is `unusable` — the weakest number in the whole system,
from any brand. Never build a conclusion on it.**

This is the clearest case for keeping the axes apart: certainty about which
device owns the bout buys nothing for the magnitude it reports.

### Rule D — self-reported intake

Calories, protein, carbs, fat, individual entries, meal timing: **the user's
own food log is the governing source.** No sensor outranks it.

Rule D sits **outside** the capability model — it is self-reported, not
sensed, so no wearable evidence bears on it. Reliability grading is by how the
entry was captured, not by a research dossier:
- `barcode` — read off a Nutrition Facts panel. Highest confidence.
- `quick` / `library` / `manual` — reference values or saved figures. Good,
  but portion size is estimated.
- `photo` — hand-portion estimate. **A rough bracket, not a measurement.** If
  a conclusion depends on one, ask for the image and re-estimate.

**Mechanics:** there is no MCP server for nutrition. It cannot be queried — it
arrives only when the user pastes it in or maintains `food-log.csv`. **If
asked about intake and nothing has been provided this session, say so and ask
for it.** Never answer from an earlier session's numbers as if current, and
never infer intake from calorie *expenditure* — burn is not intake, and
expenditure is `unusable` anyway. A nutrition endpoint on a sensor platform is
a **mirror, not a source**.

Partial logging is normal: a day showing 900 kcal usually means logging
stopped, not that 900 kcal were eaten. Flag suspected under-logging rather
than treating the total as fact.

### When a record fits no rule

When a genuinely new data type appears that doesn't fit A/B/C/D, **don't guess
silently.** Name what it is and which source produced it, say which rule it
most resembles and why it doesn't fit cleanly, and ask. Until it is
classified, report it unrouted and **do not fold it into any total or trend.**

## Deduplication — do this before any analysis

1. Before combining or summing activity data, check for **time-overlapping
   events**, across sources AND within each source.
2. Use a **±12 minute overlap buffer** — the midpoint of the 10–15 min lag
   between a real event and a passive device's auto-detection of it.
3. **Deduplicate within each source first.** A single provider can emit
   near-identical records for one event (observed: one walking bout returned
   three times, calories 56 / 56 / 55.746). Near-identical values are the
   tell, not a counter-argument. Skipping this inflates totals before any
   cross-source comparison runs.
4. **Recorded vs auto-detected**: keep the recorded version's metrics,
   **ABSORB** the auto-detected duplicate — record the merge, then drop it
   from totals.
5. **Recorded vs recorded**: still ONE event. Do not pick a single winner for
   the whole record — **merge by channel**: `event` to the recorder that
   captured it, `heart_rate` to whichever carries an `external_hr_monitor`.
   Record the merge on both and say which channel came from where.
6. **Overlap is necessary but not sufficient.** Two genuinely separate bouts
   can fall inside the buffer — a warm-up walk and the run after it. Before
   collapsing, check that activity type and duration are consistent with one
   event; if not, keep both and say why. Over-merging is as wrong as
   double-counting and harder to notice.
7. **Never average.** Averaging invents a value neither sensor measured.
8. Only count an auto-detected session as genuine incidental activity if it
   has **no** corresponding recorded activity in that window.

When computing daily totals, be explicit about which source contributed which
portion, so the math can be sanity-checked.

## Preserve disagreement

- **Never average conflicting sensors.**
- **Select a source only when a rule or an explicit tiebreak allows it.**
  Absent both, report both values with provenance and say nothing resolved it.
- **Preserve what lost** — an absorbed duplicate and an unresolved competitor
  both stay visible in the provenance.
- **"Selected" is not "correct."** Say "routed from X under Rule Y", not "X is
  correct."
- **A large disagreement inside both sensors' validated regimes is a finding**,
  not something to resolve by preference.

If the user asks you to just average two sensors: say plainly why that produces
a number neither device measured, report both with provenance, and offer the
comparison they probably want. If they reaffirm, give the mean labelled as
user-requested and not a measurement, keep both source values beside it, and
never let it become the routed value or feed a conclusion.

## Carry provenance in canonical form

Every routed number is a **routed observation**: one metric, one channel, one
window. See [`references/routed-observation.md`](references/routed-observation.md)
for the full contract and worked examples. It carries:

`metric` · `value` · `unit` · `window` · `channel` · `routing_status`
(`routed`/`unresolved`/`withheld`) · `selected_source` (device, capability
class, sensor class) · `routing` (rule, basis, decided_by) · `measurement`
(confidence, evidence, caveats) · `merged_from` · `competing` ·
`must_disclose`.

The recorder and the sensor are separate fields on purpose — a strap paired to
a ring's app is that device's record with `sensor_class: ecg_chest_strap`.

**Always surface:** every `must_disclose` entry; a basis of `provisional`,
`user_preference` or `unresolved`; a confidence of `low`, `unvalidated` or
`unusable`; any status other than `routed`; and that a merge happened whenever
a total or count is reported.

A bare number is only appropriate when the basis is `structural` or
`evidence_backed`, confidence is `high`, and nothing was merged. If you can't
say which source produced it, under which rule, and how good the number is,
say that instead of reporting it.

## Known data-source defects

**Check `devices.yaml` → `known_defects` before trusting any tool's output.**
These bugs return plausible-looking data rather than an error, so checking for
failures will not catch them.

A metric covered by an open defect is `withheld`, not routed: say the data is
unavailable and why, say what the defect makes *impossible* rather than merely
caveated, and **do not quietly route around it.** A silently wrong number is
worse than a missing one.

On finding a new defect: verify it (same request, different inputs, look for
impossible invariance), tell the user, and record it in `devices.yaml`.

## Evidence discipline

- **Never cite a study from memory.** Accuracy claims come from a dossier in
  `references/` or get read against the primary source first. This is where
  health claims quietly fail.
- **Source-quality bar, in order:** peer-reviewed validation studies (vs
  polysomnography for sleep, vs ECG for HR/HRV) > independent testers with
  published reference-device methodology > **never** vendor marketing or spec
  sheets.
- **A dossier grades measurements, not routing.** Evidence never promotes a
  device over another; capability classes decide that.
- **A new finding is never an automatic rule change.** Raise it, record it,
  then propose the edit — and log it, including reviews concluding "no
  change."

See `references/README.md` for an index of every paper cited, and
`references/rule-{a,b,c}-*.md` for the dossier behind each rule — methodology,
sample size, device generation, both confidence grades, and the gaps the
evidence leaves open. Cite from these, never from memory.

## Analytical standards

Apply to every interpretive claim, not just formal analysis requests.

- **Correlation vs causation** — say "associated with" or "coincided with,"
  not "caused by," unless there's an established mechanism. (Intense training
  suppressing next-day HRV is fine to state causally; "your stress is high
  because of afternoon coffee" is a guess.)
- **Confounders** — before attributing a change, consider illness, alcohol,
  travel/jet lag, heat, altitude, medication, caffeine timing, hormonal cycle
  phase. If you can't rule them out, say the confounder is unaddressed rather
  than ignoring it.
- **Time lag** — recovery metrics often reflect stress from 1–2 days prior.
  Check same-day, next-day, and +2 day windows rather than assuming same-day
  is right.
- **Personal baseline over population norms** — 30-day rolling window, at
  least 7 days of data before calling anything anomalous, 2σ threshold. This
  is not stylistic: given documented absolute biases such as a ~15 ms RMSSD
  underestimate and a ~9% step underestimate, a population norm compared
  against a biased absolute number is meaningless.
- **Sample-size honesty** — don't generalize from one or two occurrences. Say
  it's a hypothesis and name what data would confirm it.
- **Alternative explanations** — before settling on an interpretation, note at
  least one plausible alternative, especially at high stakes ("overtraining"
  vs "getting sick" vs "normal variability").
- **Metric limitations** — distinguish raw measurements (HR, HRV in ms) from
  proprietary composite scores (readiness, body battery, training status).
  Composites obscure what's driving a change; look at the underlying
  contributors.

## Subjective data

Workout notes, perceived effort, "feel" ratings. Treat as a **signal to
investigate**, not a fact to repeat back. They carry what sensors can't —
motivation, pain, life stress, illness onset — but are self-reported.

- Agreement with sensor data is **confirmatory** — say so.
- **Disagreement** (note says "felt easy" but HR was elevated) — flag the
  mismatch explicitly and propose explanations rather than silently picking a
  winner.
- Neither overrides the other by default. They're cross-validation, not a
  hierarchy.

## Use everything available — don't pre-filter

Before analysis, enumerate the tools every configured MCP server exposes.
Pull from any that are relevant, including less obvious ones (SpO2,
cardiovascular age, respiration rate, resilience, tags, cycle tracking). These
rules are **routing logic for when sources conflict**, not a whitelist of what
may be looked at.

Flag anomalies and pattern breaks, not just averages. Ground every observation
in actual numbers pulled from the tools — no generic textbook fitness advice.
When a tool returns nulls, say so rather than filling the gap with typical
values.

## Safety boundary

These are consumer devices and this is tooling for personal data analysis.
**Nothing here is a diagnostic instrument, and none of this is medical
advice.** Routing a number carefully does not make it clinical-grade; much of
this skill's work is establishing how *little* some numbers support. If a
question is really a medical one, say the data can describe a pattern but
cannot answer it.
