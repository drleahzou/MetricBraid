# The routed observation

The canonical internal representation of one metric after arbitration. It is
the contract between the routing rules in [`CLAUDE.md`](../../../templates/CLAUDE.md) and
anything that reports a number to a person.

Machine-readable form: [`routed-observation.schema.json`](https://github.com/drleahzou/MetricBraid/blob/main/spec/routed-observation.schema.json).
Worked examples: [`spec/examples/`](https://github.com/drleahzou/MetricBraid/blob/main/spec/examples/).

## What it is for

MetricBraid's pipeline is:

```
candidate observations → routing / arbitration → confidence → provenance → answer
```

Everything before the last arrow used to live only in prose instructions, which
made provenance a habit rather than a structure. A routed observation is the
object that carries the middle three steps forward, so that "which device
produced this, under which rule, and how much of it survives contact with the
evidence" is answerable by inspection rather than by recall.

It is deliberately small. There is no store, no id scheme, no lifecycle. Build
one per metric while analysing, keep it in working context, surface the parts
that are material. Nothing here requires persistence.

## One observation = one metric, one channel, one window

**A record is not an observation.** A recorded workout carries a distance
claim and a heart-rate claim, produced by different sensors with different
error behaviour, and the rules route them separately. So it produces at least
two routed observations that share a window and disagree about nothing,
because they are answering different questions.

This is the structural form of the framework's channel principle: **route
channels, not whole records.** Channels currently in use:

| Channel | Carries | Typical rule |
|---|---|---|
| `event` | GPS, pace, distance, duration, power, cadence, training load | B |
| `heart_rate` | In-workout HR, from whichever sensor class is present | B |
| `passive` | Sleep, resting HR, HRV, temperature, recovery scores | A |
| `incidental` | Steps, auto-detected bouts, general movement | C |
| `intake` | Self-reported food and drink | D |

Add a channel only when a real source produces a claim that an existing
channel cannot carry without lying about its provenance.

## Fields

Full types and enums are in the schema. The load-bearing ones:

- **`metric`, `value`, `unit`, `window`** — what was measured, and over what
  span. `value` is `null` whenever `routing_status` is not `routed`.
- **`selected_source`** — `device` (the id from `devices.yaml`),
  `capability_class` (the class of *this record*, not everything the device
  can do), `sensor_class`, `record_id`. The recorder and the sensor are
  separate fields on purpose: a strap paired to a phone app is
  `device: <the app's device>`, `sensor_class: ecg_chest_strap`.
  Distance, steps and active minutes use `sensor_class: not_applicable`;
  do not copy a device's HR sensor into unrelated metrics.
- **`routing`** — `rule`, `basis`, `decided_by`. This is why the source was
  selected.
- **`measurement`** — `confidence`, `evidence` (dossier paths), `caveats`.
  This is how much the number is worth.
- **`merged_from`** — competing records for the same real-world event that
  were folded in. Deduplication writes here instead of dropping.
- **`competing`** — all candidates in an unresolved disagreement, or losing
  measurements after a tiebreak. A routed preference does not erase the spread.
- **`must_disclose`** — the statements that have to reach the user when this
  observation is material to the answer.

## The two confidences are independent

`routing.basis` and `measurement.confidence` answer different questions, and
conflating them is the specific failure this model exists to prevent.

| | Question | Values |
|---|---|---|
| `routing.basis` | How firmly do we know *which source* should own this? | `structural`, `evidence_backed`, `provisional`, `user_preference`, `unresolved` |
| `measurement.confidence` | How much is *the number itself* worth? | `high`, `moderate`, `low`, `unvalidated`, `unusable` |

Every combination is reachable, and the awkward ones are the common ones:

- **`structural` + `unusable`** — a solo-detected walk's calorie figure. We
  know with certainty which device owns the bout, because nothing else saw
  it. The energy number is still the weakest in the system.
- **`structural` + `moderate`** — the same bout's step count. Certain
  attribution, ~9% systematic undercount.
- **`evidence_backed` + `high`** — HR from a declared chest strap. The
  hierarchy that selected it is cited, and so is the accuracy.
- **`evidence_backed` + `low`** — HR from a wrist sensor at high intensity
  with no external monitor. The routing is correct and cited; the number is
  known-poor, and the same citation says both.
- **`user_preference` + anything** — a `tiebreaks` entry resolved it. Routing
  is now deterministic and the measurement learned nothing. Say a tiebreak
  decided it.
- **`provisional` + `high`** — sleep duration under Rule A. Duration is well
  validated; the claim that *this class of device* should own it is reasoned
  from design, not measured.
- **`unresolved` + anything** — two sources disagree and no rule or tiebreak
  applies. `value` stays `null`, `competing` holds both, and the answer says
  so.

`unvalidated` is not `low`. `low` means applicable accepted evidence found poor
performance in this regime. `unvalidated` means no applicable validation meeting
the source-quality bar has been verified here, not that no study exists anywhere.
Ring exercise HR remains `unvalidated` under the accepted evidence; wrist HR
defaults to `low` at effort unless accepted, more specific validation applies.
Pending research does not upgrade confidence or promote the ring over the wrist.

`unvalidated` is also distinct from `unusable`: missing validation does not
establish known error or stop a capability-based source selection. `unusable`
means the requested inference cannot be supported. Confidence describes the
intended use and evidence for the candidate measurement, independently of
whether routing selected a winner. A tiebreak or an unresolved conflict does
not change that evidence. Do not invent an "Ungraded" value outside the enum.

## Routing status

- **`routed`** — a rule or tiebreak selected a source. `value` is reportable
  subject to its caveats.
- **`unresolved`** — candidates disagree, nothing resolves them. Report all of
  them with provenance. Never average, never pick quietly.
- **`withheld`** — the requested value must not be reported: a defect in
  `devices.yaml → known_defects`, a sensor declaration that is missing and
  would change the answer, or required data that isn't there. A complete
  activity total with a missing configured source is withheld, with
  `routing.basis: unresolved` because no owner can be selected and
  `measurement.confidence: unusable` for the complete-day inference.
  Available bouts retain their own confidence and can be listed as partial.
  Withholding is an explicit observation status, not a failed tool call.

## Surfacing

Provenance is carried for every routed observation. It is *reported* when it
is material — when it would change what the user does, how much they trust a
number, or whether they should believe a comparison at all.

Always surface:

- every entry in `must_disclose`
- `routing.basis` of `provisional`, `user_preference`, or `unresolved`
- `measurement.confidence` of `low`, `unvalidated`, or `unusable`
- any `routing_status` other than `routed`
- the fact that a merge happened, whenever a total or a count is reported

A bare number with none of this attached is only appropriate when the basis is
`structural` or `evidence_backed`, confidence is `high`, and nothing was
merged.

## Examples

- [`recorded-run-channel-split.json`](https://github.com/drleahzou/MetricBraid/blob/main/spec/examples/recorded-run-channel-split.json)
  — one run, two observations: the event channel from the recorder, the HR
  channel from a declared chest strap, with an overlapping auto-detection
  absorbed rather than counted twice.
- [`passive-conflict.json`](https://github.com/drleahzou/MetricBraid/blob/main/spec/examples/passive-conflict.json) — two
  devices declaring `passive_247`. The first observation is resolved by a
  tiebreak (`user_preference`, and it says so); the second has no tiebreak and
  stays `unresolved` with both values preserved.
- [`withheld-known-defect.json`](https://github.com/drleahzou/MetricBraid/blob/main/spec/examples/withheld-known-defect.json)
  — a recorded provider defect turns a plausible-looking number into a
  `withheld` observation.

## Checking

[`fixtures/check_fixtures.py`](https://github.com/drleahzou/MetricBraid/blob/main/fixtures/check_fixtures.py) in the
MetricBraid repo validates the
examples here and the routing fixtures against the enums in the schema, so the
vocabulary cannot drift between the spec, the rules and the test cases:

```bash
python3 fixtures/check_fixtures.py
```
