# Rule B — deliberately recorded workouts → the recording device wins

**Status: VERIFIED (2026-07-14) — non-provisional for the chest-strap case;
one scoped caveat for wrist-optical-recorded workouts (below).**

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

## Why this is generation-robust

The failure mode is physical, not firmware: optical PPG at the wrist is
corrupted by motion artifact and perfusion changes during exercise, while a
chest strap reads the ECG signal directly. That relationship does not change
across device generations, so — unlike Rule A — this rule does not hinge on
which specific model is paired.

## Scope and caveat

- **Chest-strap-recorded workouts:** fully supported. The recorded in-workout HR
  is the source of truth; a non-recording passive device's estimate of the same
  event loses.
- **Wrist-optical-recorded workouts** (e.g. a Garmin watch recording a run with
  no strap): the recording still wins the *event* — it is the only device that
  captured the session with GPS, pace, duration, and power — but its
  **in-workout HR carries the known wrist-optical error above.** The engine keeps
  the recorded session and its non-HR channels authoritatively; downstream
  surfaces should treat strap-less in-workout HR as lower-confidence. This
  caveat is the only reason the rule is not marked "verified, no caveats."
