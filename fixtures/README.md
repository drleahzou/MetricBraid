# Routing fixtures

Twelve adversarial cases with stated expected outcomes, in
[`routing-cases.json`](routing-cases.json).

MetricBraid's behaviour lives in prose that an assistant reads, so a prompt
edit or a model change can silently loosen a rule with nothing failing. These
fixtures are the regression surface: each one names a configuration, the
candidate records, and what the routed outcome has to be — including which
cases the system is supposed to refuse.

They are **behavioural expectations, not unit tests of code** — the subject
under test is an assistant reading a spec, not a function. So they run in two
modes: [Mode A](#running-them--mode-a-structured) grades the routing decision
deterministically and is scripted, and [Mode B](#running-them--mode-b-prose)
grades the prose a person actually reads and is still done by hand.

## Running them — Mode A, structured

[`run_fixtures.py`](run_fixtures.py) runs every case as a headless `claude -p`
session and grades the result with `==`. No judge, no flake.

```bash
python3 fixtures/run_fixtures.py
```

Each case gets a session carrying only the spec, the case's `config` rendered
as `devices.yaml`, and its `given` records — every tool and MCP server
disabled, settings off, a throwaway cwd so no other `CLAUDE.md` is discovered.
The reply is constrained by a response schema built from
[`../spec/routed-observation.schema.json`](../spec/routed-observation.schema.json),
so the vocabulary the model may answer in cannot drift from the vocabulary the
fixtures are written in.

Graded per case: `deduplication`, `abstains`, `competing_preserved`, which
metrics came back at all, and per observation the channel, `routing_status`,
rule, basis, measurement confidence, selected device, capability and sensor
class, and `merged_from`. Plus the structural half of the disclosure rule —
anything provisional, preference-decided, unresolved, weakly measured or merged
has to carry a `must_disclose` entry.

```bash
python3 fixtures/run_fixtures.py --case external-strap-beats-recorder-wrist
python3 fixtures/run_fixtures.py --spec both      # repo CLAUDE.md and the shipped skill
python3 fixtures/run_fixtures.py --model opus --json report.json
python3 fixtures/run_fixtures.py --dry-run        # print the prompts, call nothing
```

`--spec both` is the one to run before a release: it puts the same twelve cases
to `../CLAUDE.md` and to the plugin's `SKILL.md`, which is where mirror drift
would show up as a behavioural difference rather than a diff.

The runner needs a working `claude` login in the shell it runs from. It calls
the API, so it costs money and is not wired into CI.

`--self-test` is, though. It grades every case against its own expectations
(which must come back clean) and then against a deliberately mis-routed answer
(which must fail), proving the grader is still attached to the fixtures after
someone edits either. Offline, free, stdlib only.

```bash
python3 fixtures/run_fixtures.py --self-test
```

## Running them — Mode B, prose

Not automated. Mode A grades the routing decision; it cannot tell you whether
the answer a person reads discloses what it must, or quietly does something in
`must_not`. `must_not` is the part worth reading first — it is where the
plausible wrong answers are written down, and most of them are prose failures.

For one case by hand:

1. Start a session with [`../CLAUDE.md`](../CLAUDE.md) loaded — the plugin
   skill works too.
2. Give the case's `config` as the contents of `devices.yaml`, and its `given`
   records as tool output.
3. Ask the question the case implies ("what did I do this morning", "how much
   deep sleep did I get", "what was my total active time yesterday").
4. Compare the answer against `expect`:
   - Did every `must_disclose` line reach the user in some form?
   - Did it avoid everything in `must_not`?
   - If `expect.abstains` is true, did it decline to give a single number?
   - Where the case has an `on_reaffirmation`, does pushing back still hold?

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
