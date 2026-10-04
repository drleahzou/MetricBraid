# General — heart-rate sensor placement (device-agnostic)

**Applies to: every heart-rate sensor, any brand.** This is the canonical
home of the HR trust hierarchy. [Rule B](../rule-b-recorded-workouts.md)
routes its HR channel using it.

## Claim

**Sensing method and anatomical placement** underpin the conservative
in-workout HR routing hierarchy. Optical PPG is susceptible to motion artifact
and perfusion change, especially at the wrist. That mechanism does not establish
a fixed error or confidence grade for every model, generation and activity.
Brand, price and the recording app are not accuracy evidence.

## The hierarchy

Trust grades below are `measurement_confidence`, defined in
[`../routed-observation.md`](../routed-observation.md).
**`unvalidated` is not `low`**: `low` means studied and found poor in this
regime; `unvalidated` means no applicable validation meeting the source-quality
bar has been verified here. It does not mean no study exists anywhere.

| Class | Method / site | Evidence | Trust |
|---|---|---|---|
| `ecg_chest_strap` | Electrical, chest | rc **0.99** (Etiwy), rc **0.98** (Pasadyn); used as the *criterion device* by Schweizer & Gilgen-Ammann | **Highest** |
| `optical_armband` | Optical PPG, upper arm / forearm | ICC **0.99**, bias 0.27–0.33 bpm (Hettiarachchi); MAE **1.43 bpm**, MAPE 1.35%, CCC **1.00** (Schweizer, upper arm) | **High** |
| `wrist_optical` | Optical PPG, wrist | rc **0.52** (Etiwy, Garmin FR235); degrades as intensity rises (Pasadyn); MAE **6.41 bpm**, CCC 0.92 (Schweizer) | **Default low during exercise**, subject to applicable device-specific validation |
| `ring_ppg` | Optical PPG, finger | **No qualifying independent exercise validation verified here** — see gap below | **`unvalidated` under the accepted exercise evidence** |
| `other_ble` | Earbuds, gym equipment, anything broadcasting BLE HR | No citation | **`unvalidated` — treat as undeclared** |

## Evidence

All four entries read against the primary source on the dates shown.

| Date | Source | Methodology | Devices/sites | Measurement confidence |
|---|---|---|---|---|
| 2026-07-14 | Etiwy et al. 2019, *Cardiovasc Diagn Ther* ([article](https://cdt.amegroups.org/article/view/25572/24196), DOI [10.21037/cdt.2019.04.08](https://doi.org/10.21037/cdt.2019.04.08)) | vs **ECG** (Mason-Likar), n=80 cardiac-rehab patients, rest + exercise. Independent (Cleveland Clinic), no COI. | Polar H7 strap; Apple Watch; Fitbit Blaze; Garmin Forerunner 235; TomTom Spark | High |
| 2026-07-14 | Pasadyn/Gillinov et al. 2019, *Cardiovasc Diagn Ther* ([PMC6732081](https://pmc.ncbi.nlm.nih.gov/articles/PMC6732081/), DOI [10.21037/cdt.2019.06.05](https://doi.org/10.21037/cdt.2019.06.05)) | vs 3-lead **ECG**, n=50 healthy athletes, rest → treadmill ramp. Independent (Cleveland Clinic), no COI. | Polar H7 strap; Apple Watch III; Fitbit Ionic; Garmin Vivosmart HR; TomTom Spark 3 | High |
| 2026-08-30 | Hettiarachchi et al. 2019, *PLOS One* ([article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0217288), DOI [10.1371/journal.pone.0217288](https://doi.org/10.1371/journal.pone.0217288)) | vs 64-channel **ECG**, n=24, treadmill flat + 6.1° incline, spin bike 60/80 rpm. Independent (Deakin University), no competing interests. | Polar OH1 armband at **forearm, upper arm, temple** | High |
| 2026-08-30 | Schweizer & Gilgen-Ammann 2025, *JMIR Cardio* ([PMC11951816](https://pmc.ncbi.nlm.nih.gov/articles/PMC11951816/), DOI [10.2196/67110](https://doi.org/10.2196/67110)) | vs **Polar H10 ECG** criterion, n=16, nine activities from lying down to HIIT/parkour, repeated twice. Independent (Swiss Federal Institute of Sport), no COI. | Polar Verity Sense (**upper arm, forearm**) vs Polar Vantage V2 (**both wrists**) | High |

## Why this generalizes across brands

Three independent reasons, which is why this file is `general/` rather than
a per-device dossier:

1. **Multi-brand samples.** Etiwy and Pasadyn each tested five devices from
   five manufacturers and found the same wrist-optical degradation pattern.
2. **Within-brand placement split.** Schweizer & Gilgen-Ammann compared a
   Polar armband against a Polar watch, in one protocol, against one
   criterion. Arm beat wrist by ~4.5× on MAE. Brand held constant; only
   placement changed.
3. **Physical mechanism.** Motion artifact and perfusion change remain relevant
   across generations, but hardware and algorithms can change their impact.
   Placement supports the routing fallback; the error magnitude and
   measurement confidence still require applicable validation.

**Apply specific validation before the fallback.** Match device model,
generation, placement, activity, conditions and the statistic being reported.
Validation of a session average does not validate interval peaks or recovery
timing. A dossier meeting the source-quality bar can support a different grade
for that use without changing the routing hierarchy. See
[`devices/garmin.md`](../devices/garmin.md) for newer independent tester findings
and [`devices/oura.md`](../devices/oura.md) for a reviewed manufacturer-led
candidate; neither review upgrades a default grade.

## The wrist-optical penalty is intensity-dependent, not constant

This is easy to miss and changes what you may say about a low-intensity
session. Both Cleveland Clinic studies report the *same* structure:

- **At rest, the tested devices were accurate** — including wrist optical.
- Accuracy **falls as intensity rises** (Pasadyn's treadmill ramp is the
  clearest demonstration; Etiwy's rc=0.52 for one wrist device is an
  *exercise* figure, not an all-conditions one).

So a blanket "wrist optical is unreliable" overstates the case for
near-resting activity (yoga, stretching, pilates, gentle walking) and
understates how bad it gets during hard efforts and intervals. Confidence in
a strap-less HR number should scale with the session's intensity.

**A large low-intensity disagreement is worth reporting.** Agreement is a
validated cross-check only when applicable evidence covers both sensors in that
regime. Nocturnal ring validation does not establish exercise accuracy. At
higher intensity, disclose each sensor's evidence limits; their spread alone
does not establish which one is correct.

## Practical caveats that survive the good numbers

- **Armbands lag on rapid HR transitions** (intervals, sprint starts) and are
  placement-sensitive; a loose or mis-sited band degrades badly. Prefer a
  chest strap for interval work.
- **Water blocks BLE/ANT+ transmission.** For swimming, live HR from any
  external monitor generally requires onboard recording (store-and-forward)
  on the monitor itself. Check the specific model — do not assume.
- **Chest straps can misread at the very start of exercise** (dry electrodes)
  before sweat improves contact.

## Open gap — no external monitor

No qualifying independent comparison supporting promotion of ring PPG over
wrist optical during exercise has been verified here. The existence of a study
is separate from its eligibility to change a confidence grade.

**Resolution:** keep the recording device's HR. Apply accepted device-specific
validation when it covers the use; otherwise use the wrist-intensity fallbacks
in Rule B (`moderate` near rest, `low` at effort or during intervals). Ring
exercise HR remains `unvalidated` under the accepted evidence. Do **not**
promote ring PPG or infer that every current wrist sensor has the FR235's error.

**Closes when:** an independent, ECG-referenced comparison of ring PPG
during exercise is published. Tracked in [`watchlist.yaml`](https://github.com/drleahzou/MetricBraid/blob/main/evidence/watchlist.yaml).
