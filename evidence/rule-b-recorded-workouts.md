# Rule B — deliberately recorded workouts → the recording device wins

**Status: VERIFIED (2026-07-14) — non-provisional. Scope refined 2026-08-30
into a two-channel split (event vs HR) after Oura shipped Live Activity
Tracking with external strap support; see "Scope" below. One open gap
remains for no-strap sessions.**

## Claim

For a session actively recorded on a sports device — especially with a chest
strap (in-workout HR, pace, power, cadence, training load) — the recording
wins over any other device's estimate of the same event, always.

## Evidence

Both entries read against the primary source in-session on 2026-07-14. Both are
independent (Cleveland Clinic), no manufacturer funding.

| Date | Source | Methodology | Devices/generation | Confidence | Notes |
|---|---|---|---|---|---|
| 2026-07-14 | Etiwy et al. 2019, *Cardiovasc Diagn Ther* ([article](https://cdt.amegroups.org/article/view/25572/24196), DOI [10.21037/cdt.2019.04.08](https://doi.org/10.21037/cdt.2019.04.08)) | Concordance vs **ECG** (Mason-Likar), n=80 cardiac-rehab patients, rest + exercise. Independent (Cleveland Clinic; Holdsworth Fund), no COI. | Polar H7 chest strap; Apple Watch; Fitbit Blaze; **Garmin Forerunner 235**; TomTom Spark | High | Chest strap **rc=0.99** vs ECG. Wrist optical far lower during exercise: Apple 0.80, Fitbit 0.78, TomTom 0.76, **Garmin Forerunner 235 rc=0.52**. Direct evidence that a chest-strap recording beats wrist optical — and that Garmin's own wrist optical degrades badly under exercise. |
| 2026-07-14 | Pasadyn/Gillinov et al. 2019, *Cardiovasc Diagn Ther* ([PMC6732081](https://pmc.ncbi.nlm.nih.gov/articles/PMC6732081/), DOI [10.21037/cdt.2019.06.05](https://doi.org/10.21037/cdt.2019.06.05)) | Concordance vs 3-lead **ECG**, n=50 healthy athletes, rest → treadmill intensity ramp. Independent (Cleveland Clinic), no COI. | Polar H7 chest strap; Apple Watch III; Fitbit Ionic; **Garmin Vivosmart HR**; TomTom Spark 3 | High | Chest strap **rc=0.98**. All devices accurate at rest; wrist optical accuracy *falls as treadmill intensity rises*. Confirms the mechanism (motion artifact on PPG) that makes the recording device — with the option of a chest strap and direct GPS/pace/power — authoritative for the session. |
| 2026-08-30 | Hettiarachchi et al. 2019, *PLOS One* ([article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0217288), DOI [10.1371/journal.pone.0217288](https://doi.org/10.1371/journal.pone.0217288)) | vs 64-channel **ECG** (g.Nautilus), n=24 (12M/12F, 21–38y), treadmill walking flat + 6.1° incline, spin bike 60/80 rpm. Independent (Deakin University IISRI); authors declare no competing interests. | **Polar OH1 optical armband** at forearm, upper arm, temple | High | **ICC 0.99** at all three sites; mean bias **0.27–0.33 bpm**; 95% LoA ≈ ±5 bpm. Establishes that optical PPG *at the arm* is a fundamentally different accuracy regime from optical at the wrist. |
| 2026-08-30 | Schweizer & Gilgen-Ammann 2025, *JMIR Cardio* ([PMC11951816](https://pmc.ncbi.nlm.nih.gov/articles/PMC11951816/), DOI [10.2196/67110](https://doi.org/10.2196/67110)) | Head-to-head vs **Polar H10 ECG chest strap** criterion, n=16, nine activities from lying down to HIIT/parkour, protocol repeated twice. Independent (Swiss Federal Institute of Sport Magglingen); no COI declared. | **Polar Verity Sense** (upper arm, forearm) vs **Polar Vantage V2** (both wrists) | High | Upper arm: bias **−0.05 bpm**, MAE **1.43 bpm**, MAPE **1.35%**, CCC **1.00**. Non-dominant wrist: bias 2.56 bpm, MAE **6.41 bpm**, MAPE 6.82%, CCC 0.92. Same protocol, same criterion — **arm beats wrist by ~4.5× on MAE.** Note the criterion here is itself a chest strap, which is why the strap sits at the top of the hierarchy. |

## Why this is generation-robust

The failure mode is physical, not firmware: optical PPG at the wrist is
corrupted by motion artifact and perfusion changes during exercise, while a
chest strap reads the ECG signal directly. That relationship does not change
across device generations, so — unlike Rule A — this rule does not hinge on
which specific model is paired.

## Scope: two channels, routed separately

Updated 2026-08-30. The evidence supports a **channel split**, not a
single per-record winner. The event and the heart rate are different claims
with different sensors behind them.

- **EVENT channel** (GPS, pace, distance, duration, power, cadence, training
  load): the richer recorder wins, always. Fully supported — this is the only
  device that captured the session at all.
- **HR channel**: routed by **sensor class, not by brand and not by which app
  recorded the session.** The strap is the sensor; the watch or phone is only
  the recorder.

| Sensor class | Evidence | Trust |
|---|---|---|
| `ecg_chest_strap` — any BLE/ANT+ chest strap, any brand | rc=0.99 (Etiwy) / rc=0.98 (Pasadyn) vs ECG; used as the *criterion device* by Schweizer & Gilgen-Ammann | **Highest** |
| `optical_armband` — optical PPG at upper arm or forearm | ICC 0.99, bias 0.27–0.33 bpm (Hettiarachchi); MAE 1.43 bpm, CCC 1.00 (Schweizer, upper arm) | **High** |
| `wrist_optical` — watch PPG at the wrist | rc=0.52 Garmin FR235 (Etiwy); degrades as intensity rises (Pasadyn); MAE 6.41 bpm, CCC 0.92 (Schweizer) | **Low during exercise** |
| `ring_ppg` — ring PPG | **No validation during exercise exists.** [Rule A's](rule-a-passive.md) citations are nocturnal/at-rest only | **Unknown — see gap below** |
| `other_ble` — earbuds, gym equipment | No citation | **Unknown — treat as undeclared** |

**Placement is the variable, not brand.** Every reference-grade measurement
above came from a **Polar** device paired into non-Polar setups, and the
armband/wrist split in Schweizer & Gilgen-Ammann is *within a single brand* —
Verity Sense vs Vantage V2, same protocol, same criterion. Optical at the arm
and optical at the wrist are different accuracy regimes (less motion artifact,
better optical coupling), not different price points. So a third-party strap
or armband synced to a Garmin watch, or paired to the Oura app via
[Live Activity Tracking](https://support.ouraring.com/hc/en-us/articles/50433376859283-Live-Activity-Tracking)
(shipped 2026-06-04), carries that same authority.

**Two caveats that survive the good armband numbers:** optical armbands lag
during rapid HR transitions (intervals, sprint starts), and they are
placement-sensitive. For interval work a chest strap remains preferable. This
is why the two subtypes are ranked rather than treated as interchangeable.

## Open gap — sessions with no external HR monitor

When no external monitor (strap or armband) is present, the choice is
between a **known-bad** number
(wrist optical, rc≈0.52) and an **unvalidated** one (ring PPG). There is no
study comparing ring PPG against ECG *during exercise*, so the ring cannot be
promoted on evidence.

The rule therefore keeps the recording device's HR and requires an explicit
low-confidence flag. It does **not** hand HR to the ring. Swapping a
measured-poor value for an unmeasured one would look like an upgrade while
removing the ability to say how wrong it is.

**Closes when:** an independent ECG-referenced comparison of ring PPG during
exercise exists. Until then this is stated as a gap, not resolved by
preference.

## Detectability caveat (implementation, not evidence)

Neither API exposes which HR sensor fed a session. Garmin's
`device_manufacturer` names the **recorder**, not the sensor. Running dynamics
(ground contact time, vertical oscillation) are **not** a usable strap proxy on
watches that produce them from the wrist — the Forerunner 955 does. External-monitor use
must therefore be **declared by the user**, and undeclared sessions must be
treated as unmonitored for confidence purposes rather than assumed either way.
