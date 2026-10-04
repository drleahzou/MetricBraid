# Device dossier — Garmin

**Device-specific. These numbers do NOT transfer to other devices**, and note
they were measured on older models than most users will own. For the
mechanism that *does* generalize, see
[`general/hr-sensor-placement.md`](../general/hr-sensor-placement.md).

Declared capabilities: `recorded_workout`, `auto_detected`, `passive_247`.
HR sensor: `wrist_optical` for wrist-worn devices; declare placement separately
for an arm-worn sensor.

## Evidence

| Date | Source | Model tested | Measurement confidence | Notes |
|---|---|---|---|---|
| 2026-07-14 | Etiwy et al. 2019 ([DOI](https://doi.org/10.21037/cdt.2019.04.08)) | **Forerunner 235** | High | Wrist optical **rc=0.52** vs ECG during exercise — the lowest of the five devices tested (Apple 0.80, Fitbit 0.78, TomTom 0.76). Chest strap 0.99. |
| 2026-07-14 | Pasadyn/Gillinov et al. 2019 ([DOI](https://doi.org/10.21037/cdt.2019.06.05)) | **Vivosmart HR** | High | Accurate at rest; accuracy falls as treadmill intensity rises. |
| 2026-08-30 | Chinoy et al. 2021 ([DOI](https://doi.org/10.1093/sleep/zsaa291)) | **Fenix 5S**, **Vivosmart 3** | High | Included in the seven-device PSG comparison. Same class pattern as all others: high sleep sensitivity, low wake specificity, unreliable staging. |

## What these numbers oblige

- **In-workout HR without an external monitor uses the Rule B fallbacks**
  unless accepted, applicable device-specific validation supports a different
  grade. Default wrist confidence is `moderate` near rest and `low` at effort
  or during intervals. Disclose weak confidence; do not report a bare number.
- **Do not treat rc=0.52 as this generation's figure.** It was measured on a
  Forerunner 235 (2015). Newer optical sensors are likely better — but
  "likely better" is not a citation, and no independent current-generation
  quantitative error estimate has been verified here. Susceptibility to motion
  artifact persists across generations; the error magnitude does not transfer.
- **Event data is not in question.** GPS, pace, distance, duration, power and
  cadence are what a recording watch is for, and nothing above challenges
  them. Rule B's event channel stands independently of the HR channel.

## Newer independent tester evidence — Cirqa

Read 2026-10-04: [DC Rainmaker's 2026-08-03 accuracy comparison](https://www.dcrainmaker.com/2026/08/accuracy-deep-dive-garmin-cirqa-whoop-fitbit-air-amazfit-helio-polar-loop-testing.html).
Workout HR was compared simultaneously against Polar H9 or Garmin HRM-600
chest straps, with Cirqa on wrist and bicep. This meets the independent-tester
methodology tier. The article declares affiliate revenue; hardware provision
is not specified in the reviewed article. Findings are qualitative examples
from a small group, not population error estimates.

Cirqa wrist HR tracked well in several sessions but struggled in cooler
cycling and repeated running intervals; another tester had better interval
results. Bicep placement generally performed better. This supports retaining
placement and conditions as relevant, without transferring an old watch's
error to every newer device. **No default confidence grade is upgraded.**

Sleep timing used personal estimates; nightly HRV comparisons lacked a
reliable ECG reference. Those comparisons do not establish sleep-stage
accuracy, absolute HRV comparability or a passive-source ranking. The newer
Holter-validation paper remains pending full-text review in
[`CHANGELOG.md`](../CHANGELOG.md).

## Implementation notes (not evidence)

- `device_manufacturer` in the activity payload names the **recorder**, not
  the HR sensor. It cannot be used to detect strap use.
- **Running dynamics are not a strap proxy.** Ground contact time, vertical
  oscillation and stride length are produced *at the wrist* by several models
  (confirmed for the Forerunner 955). On older watches these required an
  HRM-Pro/HRM-Run or a Running Dynamics Pod, which is the origin of the
  mistaken heuristic.
