# Rule C — incidental auto-detected activity → the detecting device is the governing source

**Routing basis: `structural`.** Not a verdict about accuracy — the rule is
logically forced, because there is no competing record to reconcile against.
Attribution cannot be wrong here in the way an accuracy contest can.

**Measurement confidence: `moderate` for steps and active minutes,
`unusable` for energy expenditure.** These grades are what the citation
actually bounds, and they are unaffected by how firmly the routing is decided.

This is the clearest case for keeping the two axes apart: certainty about
*which device owns the bout* buys nothing at all for the *magnitude* it
reports. Both dimensions are defined in
[`routed-observation.md`](routed-observation.md).

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

See **[`general/activity-and-energy.md`](general/activity-and-energy.md)** —
Fuller et al. 2020, a systematic review of 158 publications and 5,934
participants across Fitbit, Garmin, Apple, Samsung, Withings and Misfit.
Device-agnostic by construction.

Headline figures: steps are the most-validated consumer metric (≈ **−9%**
mean underestimate, worse in free-living than in lab); **energy expenditure
is accurate for no brand.**

## Scope and caveat

- **Attribution:** logically forced — the detecting device owns the bout; no
  reconciliation applies. Routing basis `structural`.
- **Magnitude:** steps/active-minutes carry real error. Lab accuracy is decent
  (~45% within ±3%, biased toward underestimation); **free-living accuracy is
  materially worse** (the review notes controlled settings outperform
  free-living). Daily step and active-minute totals should therefore be treated
  as good-but-approximate, not exact — surface them as trends against the user's
  own baseline rather than precise counts. This caveat scopes the rule; it does
  not weaken the attribution, which is what Rule C actually decides.
