# Device dossier — Oura Ring

**Device-specific. These numbers do NOT transfer to other devices.** For the
baseline that applies to any consumer wearable, see
[`general/sleep-tracking.md`](../general/sleep-tracking.md) and
[`general/hr-sensor-placement.md`](../general/hr-sensor-placement.md).

Declared capabilities: `passive_247`, `auto_detected`, `recorded_workout`
(the last since Live Activity Tracking, 2026-06-04). HR sensor: `ring_ppg`.

## Evidence

All entries read against the primary source on the date shown.

| Date | Source | Methodology | Generation | Measurement confidence | Notes |
|---|---|---|---|---|---|
| 2026-07-14 | de Zambotti et al. 2019, *Behavioral Sleep Medicine* ([PMC6095823](https://pmc.ncbi.nlm.nih.gov/articles/PMC6095823/), DOI [10.1080/15402002.2017.1300587](https://doi.org/10.1080/15402002.2017.1300587)) | Epoch-by-epoch vs in-lab **PSG** (6-lead EEG, AASM), 1 night, n=41. Independent (SRI International); Oura supplied epoch data, no access to PSG staging. | **Gen1** | Medium (old generation) | Sleep sensitivity **95.5%**, wake specificity **48.1%**. Deep −20 min, REM +17 min. TST/WASO unbiased. |
| 2026-07-14 | Ghorbani/Chee et al. 2021, *Nature and Science of Sleep* ([PMC7894804](https://pmc.ncbi.nlm.nih.gov/articles/PMC7894804/), DOI [10.2147/NSS.S286070](https://doi.org/10.2147/NSS.S286070)) | Multi-night (8 nights/participant, 3 time-in-bed conditions) vs PSG, n=53. Independent (Singapore NMRC); Oura supplied rings only. | **Gen2**, fw 1.36.3 | Medium-high | Sleep-wake accuracy/sensitivity/specificity **0.88–0.89**. Deep overestimated 32–47 min; light and REM underestimated. |
| 2026-07-14 | Cao et al. 2022, *J Med Internet Res* ([PMC8808342](https://pmc.ncbi.nlm.nih.gov/articles/PMC8808342/), DOI [10.2196/27487](https://doi.org/10.2196/27487)) | Overnight HR and time/frequency-domain HRV vs Shimmer3 **ECG**, n=35. Independent (UC Irvine / U. Turku); Oura provided data access. | not stated | High (HR), Medium (HRV) | HR bias **−0.44 bpm** (r=0.999). RMSSD bias **−15 to −16 ms** (r=0.92–0.96) — good correlation, real underestimate. |

## What these numbers oblige

- **Sleep/wake duration** — trust it.
- **Sleep stages** — trend only, never stated as fact. Bias runs in *both*
  directions across generations (Gen1 underestimated deep, Gen2
  overestimated it), so not even the direction of the error is stable.
- **HRV** — trend against the user's own baseline. The ~15 ms RMSSD
  underestimate means the absolute number is **not comparable** to a clinical
  figure or to another device. The correlation is good, so *change* is
  meaningful.
- **Nocturnal only.** Every measurement above is at rest or asleep. None of
  it licenses any claim about ring HR *during exercise* — see the open gap in
  [`general/hr-sensor-placement.md`](../general/hr-sensor-placement.md).

## Uncited sub-signals

**Temperature deviation** and **all-day stress** have **no citation**. They
are named in Rule A's claim and ride it provisionally. Say so when leaning
on them.

## Contested current-generation evidence

Svensson et al. 2024, *Sleep Medicine* ([10.1016/j.sleep.2024.01.020](https://doi.org/10.1016/j.sleep.2024.01.020))
reports improved Gen3 / OSSA 2.0 staging, but carries a published
methodological critique and author response. **Recorded, deliberately not
relied upon.** This is the intended pattern: relevant evidence gets logged
even when it does not move a rule.
