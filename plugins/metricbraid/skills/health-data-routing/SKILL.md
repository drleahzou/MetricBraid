---
name: health-data-routing
description: Route and reconcile health data from multiple wearables (Oura ring, Garmin watch) when they produce overlapping or conflicting records. Use whenever the user asks about their sleep, HRV, resting heart rate, readiness, recovery, training load, VO2max, steps, workouts, stress, body battery, temperature, SpO2, or nutrition — and especially when combining, totaling, or comparing data across devices, or when asked "how am I doing", "am I recovered", "am I overtraining", or "am I getting sick". Also use when a daily total needs computing from more than one source, when two devices disagree, or when the user asks how much to trust a number.
---

# Multi-device health data routing

Two wearables produce overlapping, disagreeing claims about the same
physical events. This skill decides which source wins, prevents
double-counting, and constrains how confidently conclusions may be stated.

**If a data source fails to connect, say so before analyzing. Never
substitute assumptions for missing tool output.**

## First: read `devices.yaml`

This is **not** an Oura+Garmin skill. Which device provides which capability
is declared in the project's `devices.yaml` — **read it before routing** and
never infer hardware from which MCP servers happen to respond.

- Missing file, or a device not listed → **say so and ask.** Do not guess.
- Listing a device declares **capabilities only**. It confers no accuracy
  claim; accuracy comes only from a dossier in `references/`.
- **Devices with no dossier are normal.** Routing still works (capability
  classes are structural). For accuracy they inherit only the device-agnostic
  baselines in `references/general/`. **Never transfer a device-specific
  number to a device it wasn't measured on** — say the number is unavailable
  for that device instead.

**Two devices declaring the same class:** both `recorded_workout` → one
event, merge by channel. Both `passive_247` → use `tiebreaks` in
`devices.yaml`; if unset, report both with provenance and say the conflict is
unresolved. Never average. A tiebreak is user preference, not evidence — say
so when one decided the answer.

**A single device is valid.** Rules still apply, all resolving to one device.
Confidence goes *down*, not up: nothing cross-validates it.

## Route by capability class, not by brand

A rule never says "Oura wins sleep." It says *the passively-worn continuous
sensor wins passive signals*. Each device declares which capability classes
it has:

- **Oura** declares `passive_247` + `auto_detected` + `recorded_workout`
  (Live Activity Tracking, shipped 2026-06-04, records sessions and pairs
  external BLE heart-rate straps)
- **Garmin** declares `recorded_workout` + `auto_detected`

"Garmin records, Oura detects" is **no longer a safe assumption** anywhere.

**The RECORD carries the class, not the device.** An Oura auto-detected
walk routes through Rule C even though Oura also owns Rule A. Never name a
brand to pick a winner — name the capability that produced the record.

These are classifications by principle, not a fixed field list. Both
platforms add data types over time; classify anything new by which rule it
fits.

## The rules

### Rule A — `passive_247`: continuous passive physiological monitoring
Worn 24/7, measured passively: sleep architecture, resting HR, HRV,
temperature, readiness/recovery scores, stress, and any other passive
biometric. **The 24/7 passive sensor is the source of truth** (here: Oura).

**Status: PROVISIONAL — say so out loud when leaning on it.** Two gaps the
evidence does not close: (1) there is no independent Oura-vs-Garmin
head-to-head for passive signals — "the ring beats the watch" is reasoned
from device design, not measured; (2) current-generation staging
replication is thin and contested. Temperature deviation and all-day stress
have **no citation at all**.

What Rule A obliges in practice:
- **Sleep/wake duration** — trust it. Total sleep time is well validated.
- **Sleep stages** — do NOT present deep/REM minutes as fact. Documented
  systematic bias in both directions across generations. **Trend only.**
- **HRV** — trend against the user's own baseline, never the absolute
  value. Oura underestimates RMSSD by ~15 ms vs ECG, so the number is not
  comparable to a clinical figure or another device. The *correlation* is
  good, so *change* is meaningful.

Nutrition is explicitly **not** covered by Rule A — see Rule D.

### Rule B — `recorded_workout`: deliberately recorded sessions
**Status: VERIFIED.** Rule B routes **two channels separately** — this is
the part that is easy to get wrong.

**EVENT channel** (GPS, pace, distance, duration, power, cadence, training
load, VO2max): the device that recorded with the richer sensor set wins,
always. In this pairing that is effectively always Garmin.

**HR channel**: the **best HR sensor class present wins, regardless of which
device or app recorded the session.** Do not assume the event winner also
wins HR.

Route by sensor class **and placement** — never by brand, never by which
app recorded the session.

| Class | What it is | Trust |
|---|---|---|
| `ecg_chest_strap` | Any chest strap, any brand (Garmin HRM, Polar H10, Wahoo, any BLE HR Service strap) | **Highest** — rc=0.98–0.99 vs ECG; used as the *criterion* in other studies |
| `optical_armband` | Optical PPG at upper arm/forearm — Polar Verity Sense/OH1, Wahoo Tickr Fit, Scosche Rhythm | **High** — MAE 1.43 bpm, CCC 1.00 (upper arm); ICC 0.99 across arm sites |
| `wrist_optical` | Watch PPG at the wrist | **Low during exercise** — MAE 6.41 bpm, CCC 0.92 head-to-head; rc≈0.52; worsens as intensity rises |
| `ring_ppg` | Ring PPG | **Unknown during exercise** — no validation exists; ring evidence is nocturnal/at-rest only |
| `other_ble` | Earbuds, gym equipment, any other BLE HR broadcaster | **Unknown, uncited** — treat as undeclared |

The first two together are the routing class **`external_hr_monitor`**.
Placement is the variable, not brand or price: optical at the arm is a
different accuracy regime from optical at the wrist (less motion artifact,
better optical coupling), and beat the wrist ~4.5× on MAE in a same-brand,
same-protocol head-to-head.

Routing:
1. If any overlapping record has an `external_hr_monitor` (**either**
   subtype), **its HR wins the HR channel** even if another device won the
   event channel. An armband or strap paired to the Oura app beats an
   unmonitored Garmin watch for HR, while Garmin still owns pace/GPS/power
   for that same session.
2. If both subtypes are present (rare), prefer `ecg_chest_strap` — it is the
   reference standard the armband is validated against.
3. If no external monitor, keep the **recording device's** HR and **scale
   the confidence flag to intensity** — the wrist-optical penalty is not
   constant. Both ECG studies found all devices accurate *at rest*, with
   accuracy falling as intensity rises; rc≈0.52 is an *exercise* figure.
   - *Near-resting* (yoga, stretching, pilates, gentle walking): wrist
     optical is inside its validated-good regime. Report normally; note the
     missing monitor once, without alarm.
   - *Moderate/high intensity*: explicit low-confidence flag, in words.
   - *Intervals*: lowest non-water confidence — optical lags transitions, so
     the average can look fine while peaks and recoveries are wrong.
   - *Swimming / in-water*: unreliable from **every** sensor class. Water
     defeats wrist optical, and BLE/ANT+ does not transmit through water, so
     a strap cannot help unless it records onboard. Never compare a swim HR
     against another session's.
4. **`ring_ppg` never takes over from `wrist_optical`.** No monitor does not
   mean the ring wins — it means nobody has trustworthy in-workout HR.
   Swapping a measured-poor number for an unmeasured one is a downgrade
   disguised as an upgrade.
5. **Never average across sensor classes.**

Armbands lag on rapid HR transitions and are placement-sensitive, so a chest
strap stays preferable for interval work.

**Monitor use is not detectable from the APIs.** `device_manufacturer` names
the *recorder*, not the sensor, and running dynamics are not a proxy on
watches that generate them at the wrist (e.g. Forerunner 955). It must be
**declared by the user in `CLAUDE.md`**. If undeclared for that activity
type, say so and treat it as unmonitored for confidence — do not infer.

### Rule C — `auto_detected`: incidental activity with no matching record
Walks, chores, general movement, steps. **The detecting device is the
source of truth**, since nothing else has a record of it. Usually Oura in
this pairing, but Garmin auto-detections route here too.

**Match on the absence of a competing recorded session, not on a source
label** — Oura's `source` field returns `autodetected`, `confirmed`, and
`manual`, and a user-confirmed auto-detection is still Rule C.

**Status: VERIFIED for attribution** (logically forced — sole detector, no
competing record). **Magnitude is approximate**: consumer step counts run
~9% low on average, and free-living accuracy is materially worse than lab.
Present daily totals as trends against the user's own baseline, not exact
counts.

**Energy expenditure/calories is the weakest number in the whole system —
no consumer brand is accurate. Never build a conclusion on it.**

### Rule D — Nutrition and food intake
Calories, protein, carbs, fat, individual entries, meal timing: **the
user's own food log is the source of truth.** Neither device outranks it.

Rule D sits **outside** the capability model — it is self-reported, not
sensed, so no wearable evidence bears on it. Reliability grading is by how
the entry was captured, not by a research dossier:
- `barcode` — read off a Nutrition Facts panel. Highest confidence.
- `quick` / `library` / `manual` — reference values or saved figures. Good,
  but portion size is estimated.
- `photo` — hand-portion estimate. **A rough bracket, not a measurement.**
  If a conclusion depends on one, ask for the image and re-estimate.

**Mechanics:** there is no MCP server for nutrition. It cannot be queried —
it arrives only when the user pastes it in or maintains `food-log.csv`.
**If asked about intake and nothing has been provided this session, say so
and ask for it.** Never answer from an earlier session's numbers as if
current, and never infer intake from calorie *expenditure* — burn is not
intake. Garmin's nutrition endpoints are a **mirror, not a source**.

Partial logging is normal: a day showing 900 kcal usually means logging
stopped, not that 900 kcal were eaten. Flag suspected under-logging rather
than treating the total as fact.

### Unclassifiable data
When a genuinely new data type appears that doesn't fit A/B/C/D, don't
guess silently — flag it, name which device it came from, propose a rule,
and ask.

## Deduplication — do this before any analysis

1. Before combining or summing activity data, check for **time-overlapping
   events** between recorded activities and auto-detected sessions.
2. If they overlap, they are the **SAME real-world event**. Use a **±12
   minute overlap buffer** — the midpoint of the 10–15 min lag between a
   real event and a ring's auto-detection of it.
3. **Deduplicate within each source first.** A single provider can emit
   near-identical records for one event (observed: Oura returned one walking
   bout three times in a day, calories 56 / 56 / 55.746). Near-identical
   values are the tell, not a counter-argument. Skipping this inflates daily
   totals before any cross-source comparison runs.
4. **Recorded vs auto-detected**: keep the recorded version's metrics,
   **ABSORB** the auto-detected duplicate — record that it was merged, then
   drop it.
5. **Recorded vs recorded** (now possible — both devices record): still ONE
   event. Do not pick a single winner for the whole record — **merge by
   channel**: event channel to the richer recorder, HR channel to whichever
   carries an `external_hr_monitor`. Record `merged_from` for both and say
   which channel
   came from where.
4. **Never average the two.** Averaging invents a value neither sensor
   measured, which is worse than either.
5. Only count an auto-detected session as genuine incidental activity if it
   has **no** corresponding recorded activity in that window.

**Carry provenance on every number reported:** which source produced it,
which rule selected it, what was merged into it, and whether the governing
rule is provisional. If you can't answer "which device produced this and
under which rule," you can't defend the number.

When computing daily totals, be explicit about which source contributed
which portion, so the math can be sanity-checked.

## Known data-source defects

**Check `devices.yaml` → `known_defects` before trusting any tool's output.**
These bugs return plausible-looking data rather than an error, so checking
for failures will not catch them.

- **Oura `get_heart_rate` ignores the date range** (observed 2026-08-30):
  three different dates returned byte-identical summaries. Do not use it for
  date-specific analysis — say the data is unavailable rather than reporting
  what it returns. Oura-vs-other-device HR comparison is currently impossible.
- **Oura `get_workouts` can duplicate bouts** — run intra-source dedup first.

On finding a new defect: verify it (same request, different inputs, look for
impossible invariance), tell the user, record it, and **do not quietly route
around it.** A silently wrong number is worse than a missing one.

## Evidence discipline

- **Never cite a study from memory.** Accuracy claims come from a dossier
  in `evidence/` or get read against the primary source first. This is
  where health claims quietly fail.
- **Source-quality bar, in order:** peer-reviewed validation studies (vs
  polysomnography for sleep, vs ECG for HR/HRV) > independent testers with
  published reference-device methodology (The Quantified Scientist, DC
  Rainmaker, Marco Altini) > **never** vendor marketing or spec sheets.
- **A new finding is never an automatic rule change.** Raise it, record it,
  then propose the edit — and log it, including reviews concluding "no
  change."

See `references/README.md` for an index of every paper cited, and
`references/rule-{a,b,c}-*.md` for the dossier behind each rule —
methodology, sample size, device generation, confidence grade, and the
gaps the evidence leaves open. Cite from these, never from memory.

## Analytical standards

Apply to every interpretive claim, not just formal analysis requests.

- **Correlation vs causation** — say "associated with" or "coincided with,"
  not "caused by," unless there's an established mechanism. (Intense
  training suppressing next-day HRV is fine to state causally; "your stress
  is high because of afternoon coffee" is a guess.)
- **Confounders** — before attributing a change, consider illness, alcohol,
  travel/jet lag, heat, altitude, medication, caffeine timing, hormonal
  cycle phase. If you can't rule them out, say the confounder is
  unaddressed rather than ignoring it.
- **Time lag** — recovery metrics often reflect stress from 1–2 days prior.
  Check same-day, next-day, and +2 day windows rather than assuming
  same-day is right.
- **Personal baseline over population norms** — 30-day rolling window, at
  least 7 days of data before calling anything anomalous, 2σ threshold.
  This is not stylistic: given the ~15 ms RMSSD underestimate and ~9% step
  underestimate, a population norm compared against a biased absolute
  number is meaningless.
- **Sample-size honesty** — don't generalize from one or two occurrences.
  Say it's a hypothesis and name what data would confirm it.
- **Alternative explanations** — before settling on an interpretation,
  note at least one plausible alternative, especially at high stakes
  ("overtraining" vs "getting sick" vs "normal variability").
- **Metric limitations** — distinguish raw measurements (HR, HRV in ms)
  from proprietary composite scores (Readiness, Body Battery, Training
  Status). Composites obscure what's driving a change; look at the
  underlying contributors.

## Subjective data

Workout notes, perceived effort, "feel" ratings. Treat as a **signal to
investigate**, not a fact to repeat back. They carry what sensors can't —
motivation, pain, life stress, illness onset — but are self-reported.

- Agreement with sensor data is **confirmatory** — say so.
- **Disagreement** (note says "felt easy" but HR was elevated) — flag the
  mismatch explicitly and propose explanations rather than silently picking
  a winner.
- Neither overrides the other by default. They're cross-validation, not a
  hierarchy.

## Use everything available — don't pre-filter

Before analysis, enumerate the tools both MCP servers currently expose.
Pull from any that are relevant, including less obvious ones (SpO2,
cardiovascular age, respiration rate, resilience, tags, cycle tracking).
These rules are **routing logic for when sources conflict**, not a
whitelist of what may be looked at.

Flag anomalies and pattern breaks, not just averages. Ground every
observation in actual numbers pulled from the tools — no generic textbook
fitness advice. When a tool returns nulls, say so rather than filling the
gap with typical values.
