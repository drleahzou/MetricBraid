# Rule A — passive/continuous physiological monitoring → 24/7 passive wearable wins

**Status: PROVISIONAL — verified citations landed 2026-07-14, but two gaps keep
this rule provisional (see "Why still provisional" below).**

## Claim

For passively measured, continuous signals — sleep architecture, nightly HRV,
resting heart rate, temperature deviation, all-day stress — the device worn
continuously and designed for passive measurement (Oura ring in the v1 pairing)
is the source of truth over a training watch.

## Evidence

All entries below were read against the primary source in-session on the date
shown. Sources are independent of the manufacturer unless noted; where the
manufacturer supplied data or hardware, the arrangement is stated.

| Date | Source | Methodology | Devices/generation | Confidence | Notes |
|---|---|---|---|---|---|
| 2026-07-14 | de Zambotti et al. 2019, *Behavioral Sleep Medicine* — "The Sleep of the Ring" ([PMC6095823](https://pmc.ncbi.nlm.nih.gov/articles/PMC6095823/), DOI [10.1080/15402002.2017.1300587](https://doi.org/10.1080/15402002.2017.1300587)) | Epoch-by-epoch vs in-lab PSG (6-lead EEG, AASM scoring), 1 night, n=41 healthy adolescents/young adults. Independent (SRI International); Oura supplied epoch data but had no access to PSG staging or participant data. | Oura **Gen1** | Medium (old generation) | Sleep-detection sensitivity **95.5%**, but wake specificity only **48.1%** (poor at catching wake). Underestimated deep sleep ≈20 min, overestimated REM ≈17 min. TST/WASO unbiased. Establishes Oura as a valid *sleep/wake* passive monitor; **sleep staging is only moderate.** |
| 2026-07-14 | Chee/Ghorbani et al. 2021, *Nature and Science of Sleep* ([PMC7894804](https://pmc.ncbi.nlm.nih.gov/articles/PMC7894804/), DOI [10.2147/NSS.S286070](https://doi.org/10.2147/NSS.S286070)) | Multi-night (8 nights/participant, 3 time-in-bed conditions) vs PSG, n=53 healthy adolescents. Independent (Singapore NMRC-funded); Oura supplied rings only, "contents independently generated." | Oura **Gen2**, fw 1.36.3 | Medium-high (multi-night, but Gen2) | Sleep-wake accuracy/sensitivity/specificity **0.88–0.89**. Systematic staging bias persists: deep sleep overestimated 32–47 min, light and REM underestimated. Confirms good sleep/wake detection, imperfect staging, on a newer generation than Gen1. |
| 2026-07-14 | Cao et al. 2022, *J Med Internet Res* ([PMC8808342](https://pmc.ncbi.nlm.nih.gov/articles/PMC8808342/), DOI [10.2196/27487](https://doi.org/10.2196/27487)) | Overnight nocturnal HR and time/frequency-domain HRV vs Shimmer3 **ECG**, n=35 healthy adults. Independent (UC Irvine / U. Turku); Oura provided data access, no other conflict declared. | Oura ring (generation not stated in paper) | High for HR, Medium for HRV | HR mean bias **−0.44 bpm** (r=0.999) — excellent. RMSSD (nightly HRV) mean bias **−15 to −16 ms** (r=0.92–0.96) — good correlation but a real underestimate, so absolute HRV should be read as trend-vs-baseline, not an exact value. |

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
