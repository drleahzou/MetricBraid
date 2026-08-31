# Routing fixtures

Twelve adversarial cases with stated expected outcomes, in
[`routing-cases.json`](routing-cases.json).

MetricBraid's behaviour lives in prose that an assistant reads, so a prompt
edit or a model change can silently loosen a rule with nothing failing. These
fixtures are the regression surface: each one names a configuration, the
candidate records, and what the routed outcome has to be — including which
cases the system is supposed to refuse.

They are **behavioural expectations, not unit tests of code.** There is no
engine here to run them against.

## Running them as an eval

For one case, or for all twelve:

1. Start a session with [`../CLAUDE.md`](../CLAUDE.md) loaded — the plugin
   skill works too.
2. Give the case's `config` as the contents of `devices.yaml`, and its `given`
   records as tool output.
3. Ask the question the case implies ("what did I do this morning", "how much
   deep sleep did I get", "what was my total active time yesterday").
4. Compare the answer against `expect`:
   - Did it route to the sources named in `expect.observations`, under the
     stated `rule` and `basis`?
   - Did it deduplicate — or not — as `expect.deduplication` says?
   - Did every `must_disclose` line reach the user in some form?
   - Did it avoid everything in `must_not`?
   - If `expect.abstains` is true, did it decline to give a single number?

`must_not` is the part worth reading first. It is where the plausible wrong
answers are written down.

## Checking the fixtures themselves

```bash
python3 fixtures/check_fixtures.py --list
```

Stdlib only, no dependencies. It does not evaluate behaviour — it enforces
that every fixture and every [spec example](../spec/examples/) speaks the
vocabulary defined in
[`../spec/routed-observation.schema.json`](../spec/routed-observation.schema.json),
and that four invariants from `CLAUDE.md` hold in the expectations themselves:

- a `routed` observation names a source; an `unresolved` or `withheld` one
  does not
- an `unresolved` observation preserves the competing values, or says that no
  rule applies
- anything provisional, preference-decided, unresolved, weakly measured,
  withheld or merged carries at least one `must_disclose` entry
- every routing decision names the mechanism that made it

So a rule change that widens the vocabulary without updating the schema, or a
fixture that expects a quietly-picked winner, fails the check.

## What each case pins down

| Case | Pins down |
|---|---|
| `recorded-overlaps-autodetected` | The base double-count: one run, two records, ±12 min buffer |
| `external-strap-beats-recorder-wrist` | Channel routing — the event winner does not take the HR channel |
| `two-passive-devices-disagree-no-tiebreak` | Abstention. Two `passive_247` devices, nothing to resolve them |
| `sleep-duration-disagreement-with-tiebreak` | A resolved conflict still shows the spread |
| `single-device-setup` | Valid, and *less* confident — nothing cross-validates |
| `unclassifiable-new-metric` | Widening the model deliberately instead of by analogy |
| `integration-unavailable` | A missing source does not make the survivor an uncontested winner |
| `device-without-dossier` | Routing works; another device's numbers are not borrowed |
| `same-workout-shifted-timestamps` | Intra-source duplicates, where near-identical values are the tell |
| `close-but-separate-workouts` | The over-merge guard — overlap is necessary, not sufficient |
| `user-asks-for-an-average` | The rule survives being asked nicely to break it |
| `tiebreak-does-not-raise-confidence` | Deterministic routing ≠ a validated measurement |

## Adding a case

Copy the shape of an existing one. A case needs `id`, `title`,
`why_it_matters`, `config`, `given` and `expect`; `expect` needs
`observations`, `must_not` and `abstains`. Then run the checker.

The bar for a new fixture: **it should be able to fail.** A case that any
reasonable answer passes documents the design without defending it. The useful
ones are where the wrong answer is the fluent one.
