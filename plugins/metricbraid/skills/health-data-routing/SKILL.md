---
name: health-data-routing
description: Route and reconcile health data from multiple wearables (Oura ring, Garmin watch) when they produce overlapping or conflicting records. Use whenever the user asks about their sleep, HRV, resting heart rate, readiness, recovery, training load, VO2max, steps, workouts, stress, body battery, temperature, SpO2, or nutrition — and especially when combining, totaling, or comparing data across devices, or when asked "how am I doing", "am I recovered", "am I overtraining", or "am I getting sick". Also use when a daily total needs computing from more than one source, when two devices disagree, or when the user asks how much to trust a number.
---

# Multi-device health data routing

Two wearables produce overlapping, disagreeing claims about the same
physical events. This skill decides which source wins, prevents
double-counting, and constrains how confidently conclusions may be stated.

**If either MCP server fails to connect, say so before analyzing. Never
substitute assumptions for missing tool output.**

## Route by capability class, not by brand

A rule never says "Oura wins sleep." It says *the passively-worn continuous
sensor wins passive signals*. Each device declares which capability classes
it has:

- **Oura** declares `passive_247` + `auto_detected`
- **Garmin** declares `recorded_workout` + `auto_detected`

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
**The recording device is the source of truth** (here: Garmin) for
in-workout heart rate, pace, power, cadence, training load, VO2max, and any
new workout-analysis metric. This overrides the other device's estimate of
the same activity, always.

**Status: VERIFIED, with one scoped caveat.** The recording always wins the
EVENT — it is the only device with GPS, pace, duration, power. But
in-workout **HR** is only fully authoritative when a chest strap was worn.
Strap-less wrist-optical in-workout HR carries large documented error
(Garmin wrist optical rc≈0.52 vs ECG during exercise, vs rc≈0.99 for chest
strap). Treat it as lower-confidence and say so — especially for swims and
high-intensity work.

### Rule C — `auto_detected`: incidental activity with no matching record
Walks, chores, general movement, steps. **The detecting device is the
source of truth**, since nothing else has a record of it. Usually Oura in
this pairing, but Garmin auto-detections route here too.

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
3. Keep the recorded version for workout metrics. **ABSORB** the
   auto-detected duplicate — record that it was merged, then drop it.
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
