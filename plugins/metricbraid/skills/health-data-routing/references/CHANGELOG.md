# Evidence changelog

Every accepted change to the routing model lands here — including quarterly
reviews that conclude "no change".

## 2026-07-14 — Sprint 1 evidence verification

Compiled and **verified against primary sources in-session** the first real
citations for all three rules. Every entry was read from the actual paper on
this date; nothing cited from memory. Source-quality bar (peer-reviewed vs
PSG/ECG > independent reference-device testers > never vendor marketing) held.

**Rule B — recorded workouts: PROVISIONAL → VERIFIED (non-provisional).**
- Etiwy et al. 2019 (*Cardiovasc Diagn Ther*, Cleveland Clinic, vs ECG): chest
  strap rc=0.99; Garmin Forerunner 235 wrist optical rc=0.52 during exercise.
- Pasadyn/Gillinov et al. 2019 (*Cardiovasc Diagn Ther*, vs ECG): chest strap
  rc=0.98; wrist optical degrades as intensity rises.
- Rationale to flip: independent, ECG-referenced, and the failure mode (motion
  artifact on wrist PPG) is physical → generation-robust. One scoped caveat
  recorded in the dossier for strap-less wrist-optical in-workout HR.

**Rule C — incidental auto-detected activity: PROVISIONAL → VERIFIED
(non-provisional).**
- Fuller et al. 2020 (*JMIR mHealth uHealth*, systematic review, 158 pubs):
  step count is the most-validated consumer metric; Garmin comparable to Fitbit;
  tendency to underestimate; free-living worse than lab.
- Rationale to flip: the rule's action (attribute a solo-detected bout to the
  sole detector) is logically forced — no competing record exists, so dedup
  never fires and totals can't double-count. Citation bounds magnitude trust;
  a scoped caveat (treat totals as approximate) is recorded in the dossier.

**Rule A — passive sleep/HRV: STAYS PROVISIONAL (now with verified citations).**
- de Zambotti et al. 2019 (Gen1, vs PSG): sleep sensitivity 95.5%, wake
  specificity 48.1%, staging biases (deep −20 min, REM +17 min).
- Chee/Ghorbani et al. 2021 (Gen2, multi-night vs PSG): sleep-wake ~0.88–0.89;
  staging biases persist.
- Cao et al. 2022 (vs ECG): HR bias −0.44 bpm; RMSSD underestimate ~15 ms.
- Kept provisional because verified evidence does **not** close two gaps: (1) no
  independent Oura-vs-Garmin head-to-head for passive signals (the "wins over a
  training watch" comparison is reasoned, not measured), and (2) current-gen
  (Gen3/OSSA-2.0) independent staging replication is thin/contested. Temperature
  and all-day stress sub-signals have no citation yet.

Also: `rules.rule_is_provisional()` refactored from "all rules provisional" to a
per-rule lookup so flags can move independently, with engine tests asserting the
current A=provisional, B/C=verified state.

## 2026-07-14 — initial import

- Initial rule set (A/B/C) ported from the private personal rig. All rules
  marked **provisional**: the model originated from The Quantified Scientist's
  device testing, but citations had not yet been verified against primary
  sources. (Superseded by the verification entry above the same day.)
