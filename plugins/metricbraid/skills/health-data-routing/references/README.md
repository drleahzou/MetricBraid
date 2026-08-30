# Evidence

Every routing rule in [`CLAUDE.md`](../../../templates/CLAUDE.md) is backed by a dossier in
this directory. Each dossier records the claim, the studies behind it, the
methodology and sample size, the device generation tested, a confidence
grade, and — critically — **what the evidence does not establish.**

**Verdicts decay.** Firmware ships, generations change, and a 2019 study
describes a device nobody wears now. These rules are only trustworthy if
their evidence is kept honest, which is what the [changelog](CHANGELOG.md)
and [watchlist](watchlist.yaml) are for.

All citations were read against the primary source on the date recorded in
each dossier. **Nothing here is cited from memory.**

## The dossiers

| Rule | Covers | Status | Dossier |
|---|---|---|---|
| **A** | Passive 24/7 signals — sleep, HRV, resting HR, temperature, stress | 🟡 **Provisional** | [rule-a-passive.md](rule-a-passive.md) |
| **B** | Deliberately recorded workouts — event channel (pace/power/load) and HR channel, routed separately | 🟢 **Verified**, one open gap | [rule-b-recorded-workouts.md](rule-b-recorded-workouts.md) |
| **C** | Incidental auto-detected activity — walks, steps, general movement | 🟢 **Verified** for attribution | [rule-c-incidental.md](rule-c-incidental.md) |
| **D** | Self-reported nutrition | ⚪ No dossier — outside the capability model | *(see the skill's Rule D section)* |

Rule D is self-reported rather than sensed, so no wearable validation
research bears on it. Its reliability grading is how the entry was captured
(barcode > library/manual > photo estimate), not a research dossier.

## Every paper cited

Eight studies, all independent of the manufacturers except where noted in
the dossier.

### Rule A — passive signals (provisional)

| Study | Reference standard | n | Device gen | Key finding |
|---|---|---|---|---|
| de Zambotti et al. 2019, *Behavioral Sleep Medicine* — [PMC6095823](https://pmc.ncbi.nlm.nih.gov/articles/PMC6095823/) · [doi](https://doi.org/10.1080/15402002.2017.1300587) | In-lab PSG (6-lead EEG) | 41 | Gen1 | Sleep sensitivity 95.5%, wake specificity only 48.1%; deep −20 min, REM +17 min |
| Ghorbani/Chee et al. 2021, *Nature and Science of Sleep* — [PMC7894804](https://pmc.ncbi.nlm.nih.gov/articles/PMC7894804/) · [doi](https://doi.org/10.2147/NSS.S286070) | PSG, 8 nights/participant | 53 | Gen2 | Sleep-wake 0.88–0.89; staging bias persists (deep +32–47 min) |
| Cao et al. 2022, *J Med Internet Res* — [PMC8808342](https://pmc.ncbi.nlm.nih.gov/articles/PMC8808342/) · [doi](https://doi.org/10.2196/27487) | Shimmer3 **ECG** | 35 | not stated | HR bias −0.44 bpm (excellent); **RMSSD −15 to −16 ms** (trend, not absolute) |

### Rule B — recorded workouts (verified)

| Study | Reference standard | n | Key finding |
|---|---|---|---|
| Etiwy et al. 2019, *Cardiovasc Diagn Ther* — [article](https://cdt.amegroups.org/article/view/25572/24196) · [doi](https://doi.org/10.21037/cdt.2019.04.08) | ECG (Mason-Likar) | 80 | Chest strap **rc=0.99**; Garmin Forerunner 235 wrist optical **rc=0.52** during exercise |
| Pasadyn/Gillinov et al. 2019, *Cardiovasc Diagn Ther* — [PMC6732081](https://pmc.ncbi.nlm.nih.gov/articles/PMC6732081/) · [doi](https://doi.org/10.21037/cdt.2019.06.05) | 3-lead ECG | 50 | Chest strap rc=0.98; wrist optical degrades **as intensity rises** |

### Rule B — external HR monitors: placement beats brand (verified)

| Study | Reference standard | n | Key finding |
|---|---|---|---|
| Hettiarachchi et al. 2019, *PLOS One* — [article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0217288) · [doi](https://doi.org/10.1371/journal.pone.0217288) | 64-channel ECG | 24 | Polar OH1 optical armband: **ICC 0.99** at forearm, upper arm and temple; bias 0.27–0.33 bpm |
| Schweizer & Gilgen-Ammann 2025, *JMIR Cardio* — [PMC11951816](https://pmc.ncbi.nlm.nih.gov/articles/PMC11951816/) · [doi](https://doi.org/10.2196/67110) | Polar H10 ECG chest strap | 16 | Head-to-head, nine activities to HIIT: upper arm MAE **1.43 bpm** / CCC **1.00** vs wrist MAE **6.41 bpm** / CCC 0.92 |

These two are why the HR hierarchy is keyed on **placement**, not on
"strap or not". An optical armband is not a cheap chest strap — it is a
different accuracy regime from optical at the wrist, and it sits in the
high-trust tier alongside the chest strap.

### Rule C — incidental activity (verified)

| Study | Design | Scale | Key finding |
|---|---|---|---|
| Fuller et al. 2020, *JMIR mHealth uHealth* — [full text](https://mhealth.jmir.org/2020/9/e18694/) · [doi](https://doi.org/10.2196/18694) | Systematic review | 158 publications, 169 studies, 5,934 participants | Steps are the most-validated consumer metric (mean ≈ **−9%** underestimate); **energy expenditure is accurate for no brand** |

### Open gaps — recorded, not resolved

Tracked in [watchlist.yaml](https://github.com/drleahzou/MetricBraid/blob/main/evidence/watchlist.yaml). A gap stays open until evidence
meeting the source-quality bar closes it; it is never closed by preference.

- **Ring PPG during exercise (Rule B).** When no external HR monitor is worn, the
  choice is between a *known-bad* number (wrist optical, rc≈0.52) and an
  *unvalidated* one (ring PPG — all ring HR/HRV validation above is
  nocturnal or at-rest). No ECG-referenced study of ring PPG during exercise
  exists, so the ring is **not** promoted. The rule keeps the recording
  device's HR with a mandatory low-confidence flag.
- **Oura Live Activity Tracking accuracy (Rule B).** Shipped 2026-06-04 with
  GPS/pace and external strap support. No test meeting the source-quality
  bar yet; consumer tech-press comparisons do not qualify.

### Cited but deliberately not relied upon

- **Svensson et al. 2024**, *Sleep Medicine* ([10.1016/j.sleep.2024.01.020](https://doi.org/10.1016/j.sleep.2024.01.020)) — reports improved Gen3 / OSSA 2.0 sleep staging, but carries a published methodological critique and author response. Named in the Rule A dossier and **not** treated as settled. This is the intended pattern: relevant evidence gets recorded even when it doesn't move a rule.

## Why Rule A is still provisional

It is the rule most people would assume is safest, and it is the least
settled. Two gaps the evidence does **not** close:

1. **No independent head-to-head for passive signals.** The studies validate
   the ring against clinical references (PSG/ECG) — none compares it against
   a Garmin watch's nightly sleep and HRV. "The ring beats the watch" is
   reasoned from device design, not measured.
2. **Current-generation staging replication is thin.** The strongest
   independent evidence is Gen1/Gen2; the Gen3 evidence is contested.

Additionally, **temperature deviation and all-day stress have no citation at
all** and ride the rule provisionally.

The assistant is required to say "this is provisional" out loud whenever an
answer leans on Rule A. That obligation is the point — a rule that is
honest about being unproven is more useful than one that is quietly wrong.

## Source-quality bar

In strict order:

1. Peer-reviewed validation studies against a clinical reference — PSG for
   sleep, ECG for HR/HRV
2. Independent testers publishing their reference-device methodology
   ([The Quantified Scientist](https://www.youtube.com/@TheQuantifiedScientist),
   [DC Rainmaker](https://www.dcrainmaker.com/),
   [Marco Altini](https://marcoaltini.substack.com/))
3. **Never** vendor marketing, spec sheets, or uncited recollection

## How a rule changes

A new finding is **never** an automatic rule change.

1. Something surfaces — a new validation study, new firmware, a device swap
   (see [watchlist.yaml](https://github.com/drleahzou/MetricBraid/blob/main/evidence/watchlist.yaml) for monitored sources: weekly
   automated flags, quarterly manual review).
2. It gets raised and recorded — not silently applied.
3. Only then is a rule edit proposed.
4. The edit is logged in [CHANGELOG.md](CHANGELOG.md) — **including reviews
   that conclude "no change."** A quiet rule change is indistinguishable
   from a bug.

## Found a problem?

If a citation is misread, a study is superseded, or a rule overreaches its
evidence, please
[open an issue](https://github.com/drleahzou/MetricBraid/issues) — quoting
the dossier row you're challenging. Corrections to the evidence are more
valuable to this project than new features.

**Not medical advice.** These are consumer devices and this is tooling for
personal data analysis, not a diagnostic instrument.
