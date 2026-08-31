# Rule A — passive/continuous monitoring → the 24/7 passive sensor is the governing source

**Routing basis: `provisional`.** Citations were read against primary sources
on 2026-07-14, and they do not close the two gaps that would let this rule
claim its ordering was measured rather than reasoned (see "Why the routing
basis is provisional").

**Measurement confidence: varies by signal, and moves independently of the
routing basis.** Sleep/wake duration is `high`. Sleep staging is `low`. HRV is
`moderate` as a trend against the user's own baseline and `unusable` as an
absolute value or as a cross-device comparison. Temperature deviation and
all-day stress are `unvalidated` — no citation at all.

Both dimensions, and why they move separately, are defined in
[`../spec/routed-observation.md`](../spec/routed-observation.md).

## Claim

For passively measured, continuous signals — sleep architecture, nightly HRV,
resting heart rate, temperature deviation, all-day stress — the device worn
continuously and designed for passive measurement is the governing source over
a device that is worn for training. Which device that is comes from
`devices.yaml`, never from this file.

## Evidence

This rule's evidence now lives in two places, so that what generalizes is not
confused with what does not:

- **[`general/sleep-tracking.md`](general/sleep-tracking.md)** — the
  device-agnostic baseline. Chinoy et al. 2021 (7 devices vs PSG) and Lee et
  al. 2025 (meta-analysis, 24 studies / 798 participants / 12+ brands).
  **Applies to any consumer wearable**, and is what a setup with no device
  dossier inherits.
- **[`devices/oura.md`](devices/oura.md)** — the per-device numbers for the
  ring in the bundled reference configuration
  (de Zambotti 2019, Ghorbani/Chee 2021, Cao 2022), including the ~15 ms
  RMSSD underestimate and the generation-dependent staging bias. **These do
  not transfer to other devices.**

The key point for anyone adapting this repo: the Oura-specific findings are
**instances of the class-wide pattern**, not quirks. High sleep sensitivity
with poor wake specificity, and unreliable staging, show up across seven
unrelated devices in Chinoy. So Rule A's practical obligations — trust
duration, trend the stages, never state stages as fact — are device-agnostic
and survive a change of hardware.

## Why the routing basis is provisional

Two gaps that the read-and-verified evidence does **not** close. Note that both
are about *routing* — which class of device should own the signal — not about
whether the underlying measurements are any good. The measurement side is
separately graded above, and is in better shape than the routing side.

1. **No independent head-to-head between a 24/7 passive wearable and a
   training watch for passive signals.** The rule says the passive wearable
   *is the governing source over a training watch*; the studies above
   validate Oura against clinical references (PSG/ECG) but do not compare it to a
   Garmin watch's nightly sleep/HRV. A Garmin watch also produces these signals,
   so "wins over" is currently reasoned from device design + the exercise-HR
   literature (see [rule-b](rule-b-recorded-workouts.md), where wrist optical
   degrades), not directly measured for the passive case.
2. **Current-generation staging replication is thin.** Strongest independent
   evidence is Gen1/Gen2. The Gen3 + OSSA 2.0 study (Svensson et al. 2024,
   *Sleep Medicine*, DOI 10.1016/j.sleep.2024.01.020) reports improved staging
   but carries a published methodological critique and response (Sleep Medicine
   2024), so it is not yet cited as settled here.

Additionally: **temperature deviation** and **all-day stress** are named in the
claim but have **no citation** yet — they ride on the rule provisionally.

Routing basis moves from `provisional` to `evidence_backed` when (1) a
current-generation independent passive comparison between a 24/7 ring-class
device and a training watch exists, or (2) the current-generation staging
evidence stabilizes *and* the "governing over a training watch" comparison is
substantiated for at least sleep and nightly HRV. Neither would change the
measurement grades above; they are separate axes.

**Two devices declaring `passive_247`.** Nothing here orders one 24/7 wearable
against another. A `tiebreaks.passive_247` entry in `devices.yaml` resolves the
routing deterministically, but its basis is `user_preference` and it improves
no measurement confidence. With no tiebreak the observation is `unresolved`:
report both values with their sources.
