# Evidence

Every routing rule in [`CLAUDE.md`](../../../templates/CLAUDE.md) is backed by a dossier
here. Each records the claim, the studies behind it, methodology and sample
size, device generation, a confidence grade, and — critically — **what the
evidence does not establish.**

**Verdicts decay.** Firmware ships, generations change, a 2019 study
describes hardware nobody wears now. These rules are only trustworthy if the
evidence is kept honest, which is what the [changelog](CHANGELOG.md) and
[watchlist](watchlist.yaml) are for.

All citations were read against the primary source on the date recorded in
each dossier. **Nothing here is cited from memory, or from an abstract or
search summary alone.**

---

## Two tiers, and why it matters

This repo is not an Oura+Garmin tool. Evidence is split by **how far it
generalizes**, so that adapting it to other hardware is a bounded job rather
than a rewrite:

### 🌍 `general/` — applies to any consumer wearable

Multi-brand or mechanism-based. **Every setup inherits these, whatever you
own.** A device with no dossier of its own gets these and nothing more.

| Dossier | Covers | Basis |
|---|---|---|
| [general/sleep-tracking.md](general/sleep-tracking.md) | Sleep/wake duration, wake detection, sleep staging | 7 devices vs PSG (Chinoy); meta-analysis of 24 studies, 798 participants, 12+ brands (Lee) |
| [general/hr-sensor-placement.md](general/hr-sensor-placement.md) | The HR trust hierarchy — chest strap → armband → wrist → ring | 4 studies, 12+ devices, ECG-referenced; plus a within-brand placement split |
| [general/activity-and-energy.md](general/activity-and-energy.md) | Step counts, energy expenditure | Systematic review, 158 publications, 5,934 participants (Fuller) |

### 📟 `devices/` — specific to one device, transfers to none

| Dossier | Device |
|---|---|
| [devices/oura.md](devices/oura.md) | Oura Ring — staging bias by generation, ~15 ms RMSSD underestimate, uncited sub-signals |
| [devices/garmin.md](devices/garmin.md) | Garmin watches — model-specific wrist-optical figures, and why running dynamics are not a strap proxy |
| [devices/TEMPLATE.md](devices/TEMPLATE.md) | **Adding your device — start here** |

**A number measured on one device says nothing about another.** Where a
device dossier and a general dossier disagree, the device dossier is more
specific and wins — *for that device only*.

### 📐 Rule-level dossiers

The reasoning connecting evidence to routing decisions:

| Rule | Covers | Status | Dossier |
|---|---|---|---|
| **A** | Passive 24/7 signals — sleep, HRV, resting HR, temperature, stress | 🟡 **Provisional** | [rule-a-passive.md](rule-a-passive.md) |
| **B** | Recorded workouts — event channel and HR channel, routed separately | 🟢 **Verified**, one open gap | [rule-b-recorded-workouts.md](rule-b-recorded-workouts.md) |
| **C** | Incidental auto-detected activity | 🟢 **Verified** for attribution | [rule-c-incidental.md](rule-c-incidental.md) |
| **D** | Self-reported nutrition | ⚪ Outside the capability model | *(see the skill's Rule D section)* |

Rule D is self-reported rather than sensed, so no wearable validation bears
on it. Its reliability grading is how the entry was captured (barcode >
library/manual > photo estimate), not a research dossier.

---

## Every paper cited

Ten studies. All independent of the manufacturers except where noted in the
dossier.

### Device-agnostic — sleep

| Study | Reference | Scale | Key finding |
|---|---|---|---|
| Chinoy et al. 2021, *SLEEP* — [doi](https://doi.org/10.1093/sleep/zsaa291) · [PubMed](https://pubmed.ncbi.nlm.nih.gov/33378539/) | PSG, 3 nights | n=34, **7 devices** | Sleep sensitivity ≥0.93; wake specificity only **0.18–0.54**; **30–50% misclassification** of deep and REM |
| Lee YJ et al. 2025, *J Clin Sleep Med* — [PMC11874098](https://pmc.ncbi.nlm.nih.gov/articles/PMC11874098/) · [doi](https://doi.org/10.5664/jcsm.11460) | PSG, meta-analysis | **24 studies, 798 participants**, 12+ brands incl. Whoop, Fitbit, Apple, Garmin | TST **−16.9 min**, sleep efficiency −4.7%, WASO +13.3 min. Staging explicitly excluded as unestablished |

### Device-agnostic — heart rate by placement

| Study | Reference | n | Key finding |
|---|---|---|---|
| Etiwy et al. 2019, *Cardiovasc Diagn Ther* — [doi](https://doi.org/10.21037/cdt.2019.04.08) | ECG (Mason-Likar) | 80 | Chest strap **rc=0.99**; wrist optical 0.52–0.80 across five brands |
| Pasadyn/Gillinov et al. 2019, *Cardiovasc Diagn Ther* — [PMC6732081](https://pmc.ncbi.nlm.nih.gov/articles/PMC6732081/) · [doi](https://doi.org/10.21037/cdt.2019.06.05) | 3-lead ECG | 50 | Chest strap rc=0.98; wrist optical degrades **as intensity rises** |
| Hettiarachchi et al. 2019, *PLOS One* — [doi](https://doi.org/10.1371/journal.pone.0217288) | 64-channel ECG | 24 | Optical armband **ICC 0.99** at forearm and upper arm; bias 0.27–0.33 bpm |
| Schweizer & Gilgen-Ammann 2025, *JMIR Cardio* — [PMC11951816](https://pmc.ncbi.nlm.nih.gov/articles/PMC11951816/) · [doi](https://doi.org/10.2196/67110) | Polar H10 ECG | 16 | **Same brand, same protocol**: upper arm MAE **1.43 bpm** / CCC 1.00 vs wrist MAE **6.41 bpm** / CCC 0.92 |

### Device-agnostic — activity and energy

| Study | Reference | Scale | Key finding |
|---|---|---|---|
| Fuller et al. 2020, *JMIR mHealth uHealth* — [full text](https://mhealth.jmir.org/2020/9/e18694/) · [doi](https://doi.org/10.2196/18694) | Systematic review | 158 publications, 169 studies, **5,934 participants** | Steps most-validated (mean ≈ **−9%**); **energy expenditure accurate for no brand** |

### Oura-specific

| Study | Reference | n | Generation | Key finding |
|---|---|---|---|---|
| de Zambotti et al. 2019, *Behav Sleep Med* — [PMC6095823](https://pmc.ncbi.nlm.nih.gov/articles/PMC6095823/) · [doi](https://doi.org/10.1080/15402002.2017.1300587) | PSG | 41 | Gen1 | Sensitivity 95.5%, wake specificity 48.1%; deep −20 min, REM +17 min |
| Ghorbani/Chee et al. 2021, *Nat Sci Sleep* — [PMC7894804](https://pmc.ncbi.nlm.nih.gov/articles/PMC7894804/) · [doi](https://doi.org/10.2147/NSS.S286070) | PSG, 8 nights | 53 | Gen2 | Sleep-wake 0.88–0.89; deep **over**estimated 32–47 min (opposite direction to Gen1) |
| Cao et al. 2022, *J Med Internet Res* — [PMC8808342](https://pmc.ncbi.nlm.nih.gov/articles/PMC8808342/) · [doi](https://doi.org/10.2196/27487) | Shimmer3 ECG | 35 | not stated | HR bias −0.44 bpm; **RMSSD −15 to −16 ms** — trend, not absolute |

### Cited but deliberately not relied upon

- **Svensson et al. 2024**, *Sleep Medicine* ([10.1016/j.sleep.2024.01.020](https://doi.org/10.1016/j.sleep.2024.01.020)) — reports improved Oura Gen3 / OSSA 2.0 staging, but carries a published methodological critique and author response. Recorded in [devices/oura.md](devices/oura.md), **not** treated as settled. This is the intended pattern: relevant evidence is logged even when it does not move a rule.

---

## Open gaps — recorded, not resolved

Tracked in [watchlist.yaml](https://github.com/drleahzou/MetricBraid/blob/main/evidence/watchlist.yaml). A gap stays open until evidence
meeting the source-quality bar closes it; it is never closed by preference.

- **Ring PPG during exercise (Rule B).** With no external HR monitor, the
  choice is a *known-bad* number (wrist optical) or an *unvalidated* one
  (ring PPG — all ring validation is nocturnal or at-rest). The ring is
  **not** promoted; the recorder's HR is kept with a mandatory
  low-confidence flag.
- **No independent head-to-head for passive signals (Rule A).** The rule says
  a 24/7 passive wearable beats a training watch for sleep and HRV. No study
  compares them directly. This is **reasoned from device design, not
  measured** — which is why Rule A stays provisional for *every* pairing, not
  just this one.
- **Oura Live Activity accuracy (Rule B).** Shipped 2026-06-04 with GPS/pace
  and external monitor support. No test meeting the source-quality bar yet;
  consumer tech-press comparisons do not qualify.

## Why Rule A is still provisional

It is the rule most people would assume is safest, and it is the least
settled. Beyond the head-to-head gap above, current-generation staging
replication is thin, and **temperature deviation and all-day stress have no
citation at all** — they ride the rule provisionally.

The assistant is required to say "this is provisional" out loud whenever an
answer leans on Rule A. That obligation is the point: a rule honest about
being unproven is more useful than one quietly wrong.

## Source-quality bar

In strict order:

1. Peer-reviewed validation against a clinical reference — PSG for sleep,
   ECG for HR/HRV
2. Independent testers publishing reference-device methodology
   ([The Quantified Scientist](https://www.youtube.com/@TheQuantifiedScientist),
   [DC Rainmaker](https://www.dcrainmaker.com/),
   [Marco Altini](https://marcoaltini.substack.com/))
3. **Never** vendor marketing, spec sheets, press coverage, or uncited
   recollection

## How a rule changes

A new finding is **never** an automatic rule change.

1. Something surfaces — a new study, new firmware, a device change (see
   [watchlist.yaml](https://github.com/drleahzou/MetricBraid/blob/main/evidence/watchlist.yaml): weekly automated flags, quarterly manual
   review).
2. It is raised and recorded — not silently applied.
3. Only then is a rule edit proposed.
4. The edit is logged in [CHANGELOG.md](CHANGELOG.md) — **including reviews
   concluding "no change."** A quiet rule change is indistinguishable from a
   bug.

## Contributing

Adding a device dossier is the most useful contribution to this repo. Start
from [devices/TEMPLATE.md](devices/TEMPLATE.md); it encodes the standards
above, including the requirement to state what your evidence does *not*
establish.

If a citation here is misread, superseded, or a rule overreaches its
evidence, please [open an issue](https://github.com/drleahzou/MetricBraid/issues)
quoting the row you're challenging. Corrections to the evidence are worth
more to this project than new features.

**Not medical advice.** These are consumer devices and this is tooling for
personal data analysis, not a diagnostic instrument.
