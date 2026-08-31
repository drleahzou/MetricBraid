# General — consumer sleep tracking (device-agnostic)

**Applies to: every consumer wearable, any brand.** This is the baseline
every user of this repo inherits before any device-specific dossier is
consulted. If you are adapting MetricBraid to devices with no dossier in
`evidence/devices/`, these findings still hold.

## Claim

Consumer wearables are **good at measuring how long you slept** and **poor
at measuring which stage you were in**. They systematically over-detect
sleep (they call wake "sleep"), and they misclassify deep and REM at rates
that make individual-night stage numbers unusable as fact.

## Evidence

Both entries read against the primary source on 2026-08-30.

| Date | Source | Methodology | Devices | Measurement confidence | Notes |
|---|---|---|---|---|---|
| 2026-08-30 | Chinoy et al. 2021, *SLEEP* 44(5) zsaa291 ([article](https://academic.oup.com/sleep/article/44/5/zsaa291/6055610), [PubMed](https://pubmed.ncbi.nlm.nih.gov/33378539/), DOI [10.1093/sleep/zsaa291](https://doi.org/10.1093/sleep/zsaa291)) | vs in-lab **PSG**, n=34 healthy adults, 3 consecutive nights including a disrupted-sleep condition. | 7 devices: Fatigue Science Readiband, Fitbit Alta HR, **Garmin Fenix 5S**, **Garmin Vivosmart 3**, EarlySense Live, ResMed S+, SleepScore Max | High | Sleep **sensitivity uniformly ≥0.93** — devices reliably detect sleep. Wake **specificity only 0.18–0.54** — they are bad at catching wake, and most still beat research actigraphy (0.39). Staging is worse: all six stage-reporting devices differed significantly from PSG for light sleep, with **~30–50% misclassification of deep and REM.** |
| 2026-08-30 | Lee YJ, Lee JY, Cho JH, Kang YJ, Choi JH 2025, *J Clin Sleep Med* 21(3):573–582 ([PMC11874098](https://pmc.ncbi.nlm.nih.gov/articles/PMC11874098/), DOI [10.5664/jcsm.11460](https://doi.org/10.5664/jcsm.11460)) | **Meta-analysis**, 24 studies pooled, **798 participants**, vs PSG. Independent (Soonchunhyang University); authors report no conflicts. | Pooled across Fitbit (multiple), **WHOOP**, **Garmin**, **Apple Watch**, Xiaomi Mi Band 5, Jawbone, Basis B1, Zulu, Huami Arc, E4, Readiband, myCadian | High | Pooled bias vs PSG: **total sleep time −16.9 min** (95% CI −26.3 to −7.4), sleep efficiency **−4.7%**, sleep latency **+2.6 min**, WASO **+13.3 min**. The authors explicitly **excluded staging** from the analysis and state staging performance remains unestablished. |

## What this licenses

- **Sleep/wake duration — usable.** Bias is real (≈17 min short, pooled) but
  small relative to night-to-night variation, and consistent enough to trend.
- **Wake detection — weak everywhere.** Low specificity is a *class* property,
  not a brand failing. Be skeptical of any device's "you were awake X minutes"
  number, in either direction.
- **Sleep stages — do not present as fact, for any device.** 30–50%
  misclassification of deep/REM is not a margin you can reason over. Trend
  only, and say so.
- **This is a floor, not a ceiling.** A device with its own validated dossier
  in `evidence/devices/` may do better or worse on specific metrics. Where a
  device dossier and this file disagree, the device dossier is more specific
  and wins — but only for that device.

## Why this matters for the routing model

The per-device findings recorded in this repo are **instances of this
class-wide pattern**, not device quirks. Oura Gen1 measured 95.5% sleep
sensitivity against 48.1% wake specificity — the same high-sensitivity /
low-specificity signature Chinoy found across seven unrelated devices, and
the same staging unreliability.

This has a direct consequence for [Rule A](../rule-a-passive.md): the
instruction "trust duration, trend the stages, never state stages as fact"
is **device-agnostic and evidence-backed**. It does not depend on owning an
Oura ring. Anyone adapting this repo to other hardware inherits it.

What does **not** transfer is any specific numeric offset (e.g. one device's
RMSSD underestimate, or its particular deep-sleep bias). Those live in
`evidence/devices/` and must be re-derived per device.
