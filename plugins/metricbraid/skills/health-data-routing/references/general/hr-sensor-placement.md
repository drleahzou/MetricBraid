# General — heart-rate sensor placement (device-agnostic)

**Applies to: every heart-rate sensor, any brand.** This is the canonical
home of the HR trust hierarchy. [Rule B](../rule-b-recorded-workouts.md)
routes its HR channel using it.

## Claim

In-workout heart-rate accuracy is determined by **sensing method and
anatomical placement**, not by brand, price, or which app recorded the
session. The ordering is stable across manufacturers because the failure
mode is physical: optical PPG is corrupted by motion artifact and perfusion
change, and the wrist is the worst common site for both.

## The hierarchy

Trust grades below are `measurement_confidence`, defined in
[`../routed-observation.md`](../routed-observation.md).
**`unvalidated` is not `low`**: `low` means studied and found poor in this
regime, so you can say how wrong a number is likely to be; `unvalidated` means
nobody has looked. That distinction is what stops an unstudied sensor being
promoted over a known-imperfect one.

| Class | Method / site | Evidence | Trust |
|---|---|---|---|
| `ecg_chest_strap` | Electrical, chest | rc **0.99** (Etiwy), rc **0.98** (Pasadyn); used as the *criterion device* by Schweizer & Gilgen-Ammann | **Highest** |
| `optical_armband` | Optical PPG, upper arm / forearm | ICC **0.99**, bias 0.27–0.33 bpm (Hettiarachchi); MAE **1.43 bpm**, MAPE 1.35%, CCC **1.00** (Schweizer, upper arm) | **High** |
| `wrist_optical` | Optical PPG, wrist | rc **0.52** (Etiwy, Garmin FR235); degrades as intensity rises (Pasadyn); MAE **6.41 bpm**, CCC 0.92 (Schweizer) | **Low during exercise** |
| `ring_ppg` | Optical PPG, finger | **No exercise validation exists** — see gap below | **`unvalidated` during exercise** |
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
3. **Physical mechanism.** Motion artifact and perfusion change at the wrist
   are anatomical facts, not firmware. A new watch generation does not
   relocate the radial artery. This is why the hierarchy is expected to be
   generation-robust in a way that, say, a sleep-staging algorithm is not.

## The wrist-optical penalty is intensity-dependent, not constant

This is easy to miss and changes what you may say about a low-intensity
session. Both Cleveland Clinic studies report the *same* structure:

- **At rest, all devices were accurate** — including wrist optical.
- Accuracy **falls as intensity rises** (Pasadyn's treadmill ramp is the
  clearest demonstration; Etiwy's rc=0.52 for one wrist device is an
  *exercise* figure, not an all-conditions one).

So a blanket "wrist optical is unreliable" overstates the case for
near-resting activity (yoga, stretching, pilates, gentle walking) and
understates how bad it gets during hard efforts and intervals. Confidence in
a strap-less HR number should scale with the session's intensity.

**A useful consequence:** at near-resting intensity, wrist optical *and*
ring PPG are both inside regimes where they have been validated (see the
per-device dossiers for ring HR at rest). They should broadly agree there,
which makes a low-intensity session a genuine cross-check — and a large
disagreement a signal worth reporting. At higher intensity the comparison
loses its footing, because one sensor is known-bad and the other unvalidated.

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

When no external monitor is worn, the choice is between a **known-bad**
number (`wrist_optical`) and an **unvalidated** one (`ring_ppg`). No
ECG-referenced study of ring PPG *during exercise* exists; ring HR/HRV
validation is nocturnal or at-rest only.

**Resolution:** keep the recording device's HR with a mandatory
low-confidence flag. Do **not** promote ring PPG. Promoting an unmeasured
sensor over a measured-poor one removes the ability to say how wrong the
number is, which is a downgrade disguised as an upgrade.

**Closes when:** an independent, ECG-referenced comparison of ring PPG
during exercise is published. Tracked in [`watchlist.yaml`](https://github.com/drleahzou/MetricBraid/blob/main/evidence/watchlist.yaml).
