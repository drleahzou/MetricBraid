# Rule A — passive/continuous physiological monitoring → 24/7 passive wearable wins

**Status: PROVISIONAL — verified citations landed 2026-07-14, but two gaps keep
this rule provisional (see "Why still provisional" below).**

## Claim

For passively measured, continuous signals — sleep architecture, nightly HRV,
resting heart rate, temperature deviation, all-day stress — the device worn
continuously and designed for passive measurement (Oura ring in the v1 pairing)
is the source of truth over a training watch.

## Evidence

This rule's evidence now lives in two places, so that what generalizes is not
confused with what does not:

- **[`general/sleep-tracking.md`](general/sleep-tracking.md)** — the
  device-agnostic baseline. Chinoy et al. 2021 (7 devices vs PSG) and Lee et
  al. 2025 (meta-analysis, 24 studies / 798 participants / 12+ brands).
  **Applies to any consumer wearable**, and is what a setup with no device
  dossier inherits.
- **[`devices/oura.md`](devices/oura.md)** — the Oura-specific numbers
  (de Zambotti 2019, Ghorbani/Chee 2021, Cao 2022), including the ~15 ms
  RMSSD underestimate and the generation-dependent staging bias. **These do
  not transfer to other devices.**

The key point for anyone adapting this repo: the Oura-specific findings are
**instances of the class-wide pattern**, not quirks. High sleep sensitivity
with poor wake specificity, and unreliable staging, show up across seven
unrelated devices in Chinoy. So Rule A's practical obligations — trust
duration, trend the stages, never state stages as fact — are device-agnostic
and survive a change of hardware.

## Why still provisional

Two gaps that verified evidence does **not** yet close:

1. **No independent Oura-vs-Garmin head-to-head for passive signals.** The rule
   says the passive wearable *wins over a training watch*; the studies above
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

Flip to non-provisional when (1) a current-generation independent Oura-vs-Garmin
passive comparison exists, or (2) the Gen3/OSSA-2.0 evidence stabilizes and the
"wins over training watch" comparison is substantiated for at least sleep and
nightly HRV.
