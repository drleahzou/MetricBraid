# Rule C — incidental auto-detected activity → the detecting device wins by default

**Status: VERIFIED (2026-07-14) — non-provisional. Rule is logically forced;
the citation bounds how much to trust the numbers it attributes.**

## Claim

Activity auto-detected by a continuously worn device with no matching recorded
session (walks, chores, general movement, steps) counts as genuine incidental
activity from that device — since no other device has any record of it.

## Why this rule is logically forced

The rule's *action* — attribute an auto-detected bout to the sole device that
detected it — needs no accuracy contest, because **there is no competing
record to reconcile against.** If only one device saw the movement, that device
is definitionally the source. Dedup never fires here (nothing to merge). So the
rule cannot double-count, which is the invariant that matters for daily totals.

The empirical question is narrower: *how much do we trust the magnitude* (step
count / active minutes) that we attribute? That is what the citation bounds.

## Evidence

Read against the primary source in-session on 2026-07-14.

| Date | Source | Methodology | Devices/generation | Confidence | Notes |
|---|---|---|---|---|---|
| 2026-07-14 | Fuller et al. 2020, *JMIR mHealth uHealth* — systematic review ([full text](https://mhealth.jmir.org/2020/9/e18694/), DOI [10.2196/18694](https://doi.org/10.2196/18694)) | Systematic review: 158 publications / 169 studies / 5,934 participants; steps vs direct/observed counts in lab and free-living. Independent; one author (JL) later employed by Garmin, disclosed, after paper completion. | Consumer wearables incl. Fitbit, **Garmin**, Apple, Samsung, Withings, Misfit | High (steps), as a bound | Step count is the **most-validated** consumer metric — far better than energy expenditure ("no brand accurate," <10% within limits). In controlled settings 45% of comparisons within ±3%; overall tendency to **underestimate** (mean ≈ −9%). Garmin performs "comparably to Fitbit." |

## Scope and caveat

- **Attribution:** fully supported and logically forced — the detecting device
  owns the bout; no reconciliation applies.
- **Magnitude:** steps/active-minutes carry real error. Lab accuracy is decent
  (~45% within ±3%, biased toward underestimation); **free-living accuracy is
  materially worse** (the review notes controlled settings outperform
  free-living). Daily step and active-minute totals should therefore be treated
  as good-but-approximate, not exact — surface them as trends against the user's
  own baseline rather than precise counts. This caveat scopes the rule; it does
  not weaken the attribution, which is what Rule C actually decides.
