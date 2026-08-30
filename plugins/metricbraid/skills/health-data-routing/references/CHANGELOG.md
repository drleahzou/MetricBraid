# Evidence changelog

Every accepted change to the routing model lands here — including quarterly
reviews that conclude "no change".

## 2026-08-30 — Generalized beyond the reference pairing

Prompted by the observation that this is a public repo and the rules were
still written for one person's hardware. **No verdict changed.** Two new
device-agnostic dossiers were added and existing evidence was reorganized by
how far it generalizes.

**New evidence — device-agnostic sleep tracking (2 citations, both read
against the primary source).**
- Chinoy et al. 2021, *SLEEP* 44(5) ([10.1093/sleep/zsaa291](https://doi.org/10.1093/sleep/zsaa291)):
  seven consumer devices vs PSG, n=34, 3 nights. Sleep sensitivity **≥0.93**;
  wake specificity **0.18–0.54**; **30–50% misclassification** of deep and REM.
- Lee YJ et al. 2025, *J Clin Sleep Med* ([10.5664/jcsm.11460](https://doi.org/10.5664/jcsm.11460)):
  meta-analysis, **24 studies / 798 participants**, 12+ brands including
  Whoop, Fitbit, Apple and Garmin. TST **−16.9 min**, sleep efficiency
  −4.7%, WASO +13.3 min. Staging explicitly excluded as unestablished.

**Why this matters more than the numbers:** the Oura-specific findings this
repo already carried are **instances of a class-wide pattern**, not device
quirks. High sleep sensitivity with poor wake specificity, and unreliable
staging, recur across seven unrelated devices. So Rule A's practical
obligations — trust duration, trend the stages, never state stages as fact —
are now **device-agnostic and evidence-backed**, and survive a change of
hardware. Previously a non-Oura user inherited nothing.

**Evidence restructured into two tiers.**
- `evidence/general/` — multi-brand or mechanism-based; inherited by every
  setup regardless of hardware. Three dossiers: sleep tracking, HR sensor
  placement (the hierarchy lifted out of Rule B, where it was buried), steps
  and energy expenditure.
- `evidence/devices/` — per-device numbers that transfer to nothing else
  (Oura's RMSSD offset and staging bias; Garmin's model-specific
  wrist-optical figures). Plus `TEMPLATE.md` for contributions.
- Rule dossiers keep the reasoning and cite the tables rather than
  duplicating them, so a fact has one home and cannot drift.

**Rules de-hardcoded.** Rule A said "(in this pairing, Oura)"; the capability
preamble named both devices. Capability-to-device binding now comes from a
new **`devices.yaml`** registry — the only file most users need to edit.
Ships with commented presets for Whoop, Apple Watch, Fitbit, Polar, Coros,
Suunto and Samsung. Presets declare **capabilities only**; they carry no
accuracy claims, since none has a dossier.

**New cases handled explicitly:**
- *Devices with no dossier* — route normally, inherit `general/` only, and
  **never** borrow another device's numbers.
- *Two devices, same class* — `tiebreaks` in `devices.yaml`; if unset, report
  both with provenance rather than picking silently. A tiebreak is user
  preference, not evidence, and must be declared as such. (There is no study
  establishing that one 24/7 wearable beats another for passive signals —
  this is the same gap that keeps Rule A provisional, now stated as applying
  to *every* pairing rather than just the reference one.)
- *Single-device setups* — valid, but confidence goes **down**: nothing
  cross-validates, and dedup across sources becomes a no-op.

**Limitation recorded, not hidden.** The rules are device-agnostic; the
bundled MCP servers are not — only Oura and Garmin ship. Other hardware needs
a community MCP server or manual export. The README states this plainly and
notes Rule D (nutrition) has always worked this way, which is the proof it
degrades gracefully.

## 2026-08-30 — Rule B split into event and HR channels

Prompted by a user question about setups without a chest strap, third-party
straps, and Oura's new recording capability. **No new accuracy evidence was
introduced** — this re-scopes existing citations and records a gap.

**Device change (verified against the vendor, 2026-08-30):** Oura shipped
**Live Activity Tracking** on 2026-06-04 (Gen3+), which records workouts with
live GPS/pace and supports **external BLE heart-rate straps**. The ring does
not stream live HR without an external monitor paired. This means Oura now
declares `recorded_workout` in addition to `passive_247` and `auto_detected`,
so "Garmin records, Oura detects" is no longer a safe assumption anywhere in
the model.

**Rule B: VERIFIED → VERIFIED (scope refined, status unchanged).**
- Split into an **EVENT channel** (richer recorder wins — unchanged) and an
  **HR channel** (best sensor class wins, regardless of recorder).
- Rationale from existing citations: both reference-grade measurements
  (Etiwy rc=0.99, Pasadyn rc=0.98) came from a **Polar H7** strap in non-Polar
  setups. The evidence was always about the *sensor class*, never the
  manufacturer. The previous wording ("Garmin is the source of truth") encoded
  a brand where the model claims to encode a capability — an internal
  inconsistency, now fixed. Rule A was de-branded the same way.
- Consequence: a third-party strap synced to a Garmin watch carries full
  authority, and a strap paired to the **Oura** app beats a strap-less Garmin
  watch for HR while Garmin still owns pace/GPS/power for the same session.

**New evidence — optical armbands are their own tier (2 citations added,
both read against the primary source 2026-08-30).** Prompted by the question
"does 'chest strap' include arm-worn monitors?" — it does not, and the
distinction is load-bearing:
- Hettiarachchi et al. 2019, *PLOS One* ([10.1371/journal.pone.0217288](https://doi.org/10.1371/journal.pone.0217288)):
  Polar OH1 at forearm/upper arm/temple vs 64-channel ECG, n=24. ICC **0.99**
  at all sites, bias **0.27–0.33 bpm**.
- Schweizer & Gilgen-Ammann 2025, *JMIR Cardio* ([10.2196/67110](https://doi.org/10.2196/67110)):
  Verity Sense (arm) vs Vantage V2 (wrist) against a Polar H10 ECG criterion,
  n=16, nine activities to HIIT. Upper arm MAE **1.43 bpm** / CCC **1.00**;
  wrist MAE **6.41 bpm** / CCC 0.92. **Arm beats wrist ~4.5× on MAE in the
  same protocol, within the same brand.**

Consequence: the HR hierarchy is keyed on **placement**, not on strap-vs-not.
`external_hr_monitor` becomes the routing class with two ranked subtypes —
`ecg_chest_strap` (highest; it is the criterion the armband is validated
against) and `optical_armband` (high). Armbands are **not** demoted to the
wrist tier. Two caveats recorded: armbands lag on rapid HR transitions and
are placement-sensitive, so a chest strap stays preferable for intervals.
A fifth class `other_ble` (earbuds, gym equipment) is defined as uncited and
treated as undeclared.

**New recorded gap — in-workout HR with no external monitor.** Choice is between a known-bad
value (wrist optical, rc≈0.52) and an unvalidated one (ring PPG — Rule A's
citations are nocturnal/at-rest only; there is **no** ECG-referenced study of
ring PPG during exercise). Resolution: keep the recording device's HR with a
mandatory low-confidence flag; **do not** promote ring PPG. Closes only when
an independent ECG-referenced exercise comparison for ring PPG exists. Added
to `watchlist.yaml`.

**Rule C: clarified, not changed.** Matching was described in terms of
"auto-detected", but Oura's `source` field returns `confirmed` for
user-confirmed detections (all workouts in the test account carried
`confirmed`, never `autodetected`). Rule C now matches on **the absence of a
competing recorded session**, not on a source label. Status stays VERIFIED —
this corrects a description, not a verdict.

**Deduplication: two cases added.**
- *Recorded vs recorded* — now possible via Oura Live Activity. Merge by
  channel rather than picking one record; `merged_from` records both.
- *Duplicates within a single source* — observed in live data: Oura returned
  one `walking 1:11–1:38 PM` bout **three times** on 2026-08-28 (calories
  56 / 56 / 55.746), and a second bout three times the same day. Dedup
  previously only compared across providers, so these inflated daily totals.
  Intra-source dedup now runs first.

**Implementation note (not evidence):** neither API exposes the HR sensor.
`device_manufacturer` names the recorder. Running dynamics are not a strap
proxy on a Forerunner 955, which generates them at the wrist. Strap use is
therefore user-declared, and undeclared sessions count as no-strap for
confidence purposes.

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
