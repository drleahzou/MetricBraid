# Ririhealth — Personal Health Data Analysis

This project integrates two health data sources via MCP servers (configured in
`.mcp.json`):

- **Garmin Connect** (`garmin` server — Taxuspt/garmin_mcp, 110+ tools):
  recorded activities, training load (CTL/ATL/TSB), VO2max, HRV, resting HR,
  sleep, stress, Body Battery, workout detail, and more.
- **Oura Ring** (`oura` server — mitchhankins01/oura-ring-mcp, ~27 tools):
  daily sleep, readiness, HRV, resting HR, activity, auto-detected sessions,
  temperature, stress, SpO2, resilience, cardiovascular age, tags, and more.

Every session in this project MUST follow the rules below without being
re-told. If either MCP server fails to connect, say so before analyzing —
never substitute assumptions for missing tool output.

## DATA SOURCE OF TRUTH

These are rule-based classifications by PRINCIPLE, not a fixed field list —
both apps add new data types over time (e.g. a new Garmin recovery metric),
so classify new data by which rule it fits, not by memorizing today's
feature set.

**Route by capability class, not by brand.** A rule never says "Oura wins
sleep"; it says "the passively-worn continuous sensor wins passive signals,"
and each device declares which capability classes it has. Oura declares
`passive_247` + `auto_detected`; Garmin declares `recorded_workout` +
`auto_detected`. The RECORD carries the class, not the device — so an Oura
auto-detected walk routes through Rule C even though Oura also owns Rule A.
Never name a brand to pick a winner; name the capability that produced the
record.

- **Rule A — `passive_247`: passive/continuous physiological monitoring**
  (worn 24/7, measured passively): **Oura is the source of truth.** This
  covers sleep architecture, resting HR, HRV, temperature, readiness/recovery
  scores, stress, and any other passive biometric Oura measures now or adds
  in future. **Status: PROVISIONAL — say so when leaning on it** (see
  EVIDENCE STATUS below). **Nutrition is explicitly NOT covered by this rule
  — see Rule D.** If Oura ships meal/nutrition tracking, it does not become
  the source of truth for intake; at most it is a cross-check against Rule D.
- **Rule B — `recorded_workout`: deliberately recorded sessions**: **Garmin
  is the source of truth** for any session actively recorded on the device —
  in-workout heart rate, pace, power, cadence, training load, VO2max, and any
  new workout-analysis metric Garmin adds. This overrides Oura's estimate of
  the same activity, always, regardless of what the metric is called.
  **Status: VERIFIED, with one scoped caveat** — the recording always wins
  the EVENT (it is the only device with GPS, pace, duration, power), but
  in-workout **HR** is only fully authoritative when the HRM chest strap was
  worn. Strap-less wrist-optical in-workout HR carries a large documented
  error (Garmin wrist optical rc≈0.52 vs ECG during exercise) — treat it as
  lower-confidence and say so, especially for swims and high-intensity work.
- **Rule C — `auto_detected`: incidental activity with no matching recorded
  session** (walks, chores, general movement, steps, and any new
  auto-detected activity type either device adds): **the detecting device is
  the source of truth**, since nothing else has a record of it. In this
  pairing that is usually Oura, but Garmin auto-detections route here too.
  **Status: VERIFIED for attribution** (logically forced — sole detector, no
  competing record). **Magnitude is approximate**: consumer step counts run
  ~9% low on average and free-living accuracy is materially worse than lab,
  so present daily totals as trends against their own baseline, not exact
  counts. **Energy expenditure/calories is the weakest number in the whole
  system — no consumer brand is accurate. Never build a conclusion on it.**
- **Rule D — Nutrition and food intake** (calories, protein, carbs, fat,
  individual food entries, meal timing): **the user's own food log is the
  source of truth** — whatever logger they maintain by hand (a phone app, a
  spreadsheet, `food-log.csv` in this repo). Neither device outranks it. This holds even though no MCP server
  exposes it, which has consequences for how the data arrives — see
  NUTRITION DATA INTAKE below. **Rule D sits OUTSIDE the capability model**:
  it is self-reported, not sensed, so none of the three capability classes
  covers it and no wearable evidence bears on it. Its reliability grading is
  the `Source` column (barcode > quick/library/manual > photo), not a
  research dossier.
- When a genuinely new data type appears from either device that doesn't
  obviously fit Rule A/B/C (e.g. a new Oura feature that isn't passive
  monitoring, activity, or nutrition), don't guess silently — flag it to the
  user (see STAY CURRENT below), ask which rule it should follow, then
  propose adding it to this file.

## NUTRITION DATA INTAKE (Rule D mechanics)

Unlike Garmin and Oura, the nutrition source of truth has **no MCP server**.
It cannot be queried. This changes the failure mode, so handle it explicitly:

- Food data arrives only when the user pastes it in or drops an export
  into the repo. `food-log.example.csv` shows the expected header; copy it
  to `food-log.csv` (gitignored) and fill it in.
- **If asked about intake and nothing has been pasted this session, say so
  and ask for it.** Do not answer from an earlier session's numbers as if
  they were current, and never infer intake from Garmin/Oura calorie
  *expenditure* — burn is not intake.
- Weight entries by how they were captured, which the export's `Source`
  column records:
  - `barcode` — copied off a physical Nutrition Facts panel. Highest
    confidence.
  - `quick` / `library` / `manual` — USDA reference values or the user's own
    saved figures. Good, but portion size is still estimated.
  - `photo` — hand-portion estimate, tagged `Est` in the app. **Treat as a
    rough bracket, not a measurement.** The photo is usually retained
    in the logging app, so if a conclusion depends on one of these, ask for
    the image and re-estimate rather than trusting the logged number.
- Garmin's nutrition endpoints (`get_nutrition_daily_food_log`, `log_food`)
  are a **mirror, not a source**. They are only populated if we deliberately
  push a pasted batch there. If Garmin's food log ever disagrees with the user's
  own log, the user's log wins, and the Garmin copy is stale.
- Say which day's data you actually have. Partial logging is normal — a day
  with 900 kcal recorded usually means they stopped logging, not that they ate
  900 kcal. Flag suspected under-logging instead of treating the total as
  fact.

## EVIDENCE STATUS AND DISCIPLINE

Verdicts decay — firmware ships, generations change, a 2019 study describes a
device nobody wears now. The rules above are only trustworthy if their
evidence is kept honest. Dossiers live in `evidence/`
(citations verified against primary sources 2026-07-14).

- **Rule A is PROVISIONAL and that must be VISIBLE, not smoothed over.** Two
  gaps the evidence does not close: (1) there is **no independent
  Oura-vs-Garmin head-to-head for passive signals** — "the ring beats the
  watch for sleep/HRV" is reasoned from device design, not measured; (2)
  current-generation (Gen3 / OSSA 2.0) staging replication is thin and
  contested. **Temperature deviation and all-day stress have no citation at
  all** and ride the rule provisionally. When an answer leans on Rule A, say
  the verdict is provisional.
- **What Rule A obliges in practice:**
  - *Sleep/wake duration* — trust it. Total sleep time is well validated.
  - *Sleep stages* — do NOT present deep/REM minutes as fact. Documented
    systematic bias in both directions across generations. Trend only.
  - *HRV* — trend against their own baseline, never the absolute value. Oura
    underestimates RMSSD by ~15 ms vs ECG, so the number is not comparable to
    a clinical figure or another device; the correlation is good, so *change*
    is meaningful.
- **Source-quality bar, in order:** peer-reviewed validation studies (vs
  polysomnography for sleep, vs ECG for HR/HRV) > independent testers with
  published reference-device methodology (The Quantified Scientist, DC
  Rainmaker, Marco Altini) > **never** vendor marketing, spec sheets, or
  uncited recollection.
- **Never cite a study from memory.** If a claim about device accuracy
  matters to an answer, it comes from a dossier in `evidence/` or it gets
  read against the primary source first. This is where health claims quietly
  fail.
- **A new finding is never an automatic rule change.** If something relevant
  surfaces (new validation study, new firmware, a device change), raise it,
  record it, and only then propose a rule edit — and log the edit in
  `evidence/CHANGELOG.md`, including reviews that conclude "no change."

## USE EVERYTHING AVAILABLE — DON'T PRE-FILTER

- Before analysis, enumerate the full list of tools/resources currently
  exposed by both the Garmin and Oura MCP servers (not just the metrics
  named in this file). Pull from any that are relevant to the question,
  including newer or less obvious ones (e.g. SpO2, cardiovascular age,
  respiration rate, meal/nutrition logs, tags, cycle tracking, workouts,
  resilience score, etc. — whatever currently exists).
- Treat this file as a set of ROUTING RULES for when sources conflict or
  overlap, not a whitelist of what you're allowed to look at. If a data type
  isn't mentioned here but is available and relevant, use it.

## DEDUPLICATION LOGIC (critical — do this before any analysis)

- Before combining or summing activity data, check for time-overlapping
  events between Garmin's recorded activities and Oura's auto-detected
  sessions/workouts.
- If a Garmin activity and an Oura auto-detected session overlap in
  start/end time, treat them as the SAME real-world event. **Use a ±12 minute
  overlap buffer** — the midpoint of the 10–15 min lag between a real event
  and a ring's auto-detection of it. Keep Garmin's
  version for workout metrics (HR, pace, power, calories for that session)
  and ABSORB Oura's duplicate entry — record that it was merged, then drop
  it. **Never average the two**: averaging invents a value neither sensor
  measured, which is worse than either.
- Only count an Oura auto-detected session as genuine incidental activity if
  it has no corresponding Garmin activity in that time window.
- **Carry provenance on every number you report**: which source produced it,
  which rule selected it, what (if anything) was merged into it, and whether
  the governing rule is provisional. If you can't answer "which device
  produced this and under which rule," you can't defend the number.
- When calculating daily totals (calories, active time, steps), be explicit
  about which source contributed which portion, so the user can sanity-check
  the math if a total looks off.

## ANALYSIS PHILOSOPHY

- The goal is understanding the INTERPLAY between systems, not just
  reporting numbers. When asked about any single metric, proactively note
  relevant cross-domain connections if they exist in the data — e.g. how a
  hard Garmin-recorded session affected next-day Oura HRV/readiness, how
  sleep debt correlates with training load tolerance, how incidental daily
  movement (Oura) affects recovery on top of deliberate training (Garmin),
  or how stress trends precede dips in performance.
- Always cite which device/source a number came from when it's not obvious.
- Flag anomalies or notable pattern breaks, not just averages.
- Avoid generic textbook fitness advice — ground every observation in the
  user's actual numbers pulled from the tools, not assumptions.
- When data is missing or a tool call returns nulls, say so explicitly
  rather than guessing or filling gaps with typical values.

## STAY CURRENT WITH DEVICE UPDATES

- At the start of any new session (or if the user asks "what's new"),
  briefly check whether the Garmin or Oura MCP servers expose any tools,
  resources, or data fields that aren't reflected in this file's known
  categories.
- If you notice something new — a new metric, a new tool, a new data
  category (e.g. Garmin adding a new recovery metric, Oura adding a new
  passive biometric) — tell the user proactively: name what's new, which
  device it came from, and suggest which Rule (A/B/C) it should fall under.
- Don't silently start or stop using a data type without mentioning it once.
  After the user confirms how to classify it, update this file so the rule
  persists.
- This check should be lightweight — a quick scan of available tools, not a
  deep audit every time — so it doesn't slow down normal queries.

## SUBJECTIVE / QUALITATIVE DATA

(Workout notes, perceived effort, "feel" ratings, any free-text the user
enters.)

- Treat these as a SIGNAL to investigate, not a fact to simply repeat back.
  They carry information the sensors can't capture — motivation, pain, life
  stress, illness onset — but they're also self-reported and subject to
  bias, so weigh them against the quantitative data rather than accepting or
  dismissing them outright.
- When a note/feel rating and the sensor data agree, that's confirmatory —
  say so, it strengthens confidence in the read.
- When they DISAGREE (e.g. the note says "felt easy" but HR was elevated
  throughout, or "rough session" but metrics look unremarkable), flag the
  mismatch explicitly and propose plausible explanations (heat, dehydration,
  incomplete recovery, illness incubating, poor sleep the prior night, life
  stress not captured by any device, or a sensor artifact) rather than
  silently picking one source as "correct."
- Use qualitative notes to help explain WHY a quantitative anomaly happened,
  and use quantitative data to sanity-check WHETHER a qualitative impression
  is backed by physiology. Neither one overrides the other by default —
  they're cross-validation, not a hierarchy.

## ANALYTICAL STANDARDS

(Apply to every interpretive claim, not just formal "analysis" requests —
this governs HOW to reason about the data, not just which data to use.)

- **Correlation vs. causation**: describe observed relationships as
  "associated with" or "coincided with," not "caused by," unless there's an
  established physiological mechanism (e.g. it's well-established that
  intense training suppresses next-day HRV — that's fine to state causally;
  "your stress score is high because you had coffee at 3pm" is a guess
  unless the data actually supports it).
- **Confounders**: before attributing a change in one metric to another
  (e.g. "your HRV dropped because of Tuesday's workout"), consider and rule
  out other explanations where possible — illness, alcohol, travel/jet lag,
  heat, altitude, medication or supplement changes, caffeine timing,
  hormonal cycle phase (if tracked), poor sleep environment. If you don't
  have data to rule these out, say the confounder is unaddressed rather than
  ignoring it.
- **Time lag matters**: recovery and readiness metrics often reflect stress
  from 1–2 days prior, not the same day. When looking for training-recovery
  relationships, check multiple lag windows (same-day, next-day, +2 days)
  rather than assuming same-day correlation is the right one.
- **Personal baseline over population norms**: compare the user's metrics to
  THEIR OWN rolling historical average and typical variability range, not
  generic "normal" ranges — HRV, resting HR, and readiness are highly
  individual, and a number that's "low" for the general population may be
  entirely normal for this user, or vice versa. Default parameters:
  **30-day rolling window, at least 7 days of data before calling anything
  anomalous, 2σ threshold.** This isn't a
  stylistic preference — given Oura's ~15 ms RMSSD underestimate and the ~9%
  step underestimate, **their own history is the only valid reference frame**;
  a population norm compared against a biased absolute number is meaningless.
- **Sample size honesty**: don't generalize a pattern from one or two
  occurrences. If something looks like a trend but is based on limited data
  points, say so explicitly, describe it as a hypothesis rather than a
  conclusion, and suggest what additional data would confirm or refute it.
- **Consider alternative explanations**: before settling on the most likely
  interpretation of a pattern, briefly note at least one plausible
  alternative, especially when the stakes of the conclusion are high (e.g.
  "you're overtraining" vs. "you're getting sick" vs. "this is normal
  week-to-week variability").
- **Metric limitations**: distinguish raw physiological measurements (HR,
  HRV in ms, sleep stage durations) from proprietary composite scores (Oura
  Readiness, Garmin Training Status/Body Battery). Composite scores are
  useful summaries but can obscure what's actually driving a change — when
  relevant, look at the underlying contributors to a score rather than just
  reporting the score itself.

## AUTHENTICATION NOTES

- **Garmin**: tokens live in `~/.garminconnect/` (created by running
  `garmin-mcp-auth` interactively — supports MFA; tokens last ~6 months).
  Alternatively `GARMIN_EMAIL`/`GARMIN_PASSWORD` env vars work
  non-interactively for accounts without MFA. If the garmin server exits at
  startup, authentication is the first thing to check. See `SETUP.md`.
- **Oura**: requires the `OURA_ACCESS_TOKEN` env var, which must be an
  **OAuth2 access token**.
  - **Personal Access Tokens (PATs) are dead. Oura deprecated them in
    Dec 2025 — newly generated PATs return 401 and DO NOT WORK.** The PAT
    page still exists and still hands out tokens, which is why this trap
    catches people. If a PAT is what's in the env var, no amount of
    regenerating will fix it. Tokens minted before the deprecation still
    work but cannot be replaced once revoked.
  - **Never advise regenerating or deleting a token as a first move.** If a
    pre-deprecation PAT is still working, deleting it is irreversible —
    there is no way to mint a replacement PAT. Migrate to OAuth2 instead.
  - Get an OAuth2 token by registering a personal application at
    https://cloud.ouraring.com/applications with a localhost redirect URI,
    then completing the authorization code flow. OAuth access tokens are
    sent as the same `Bearer` token against the v2 API, but they **expire
    in ~24h**, so a refresh step is required for unattended use. See
    `SETUP.md`.
  - **On any Oura 401, debug in this order — never jump to "get a new
    token":** (a) confirm the env var is actually visible to the MCP server
    process, not just to your interactive shell; (b) curl the v2 API and
    print ONLY the HTTP status, never the token; (c) check whether the
    token is a PAT (dead) or OAuth2 (refreshable); (d) if OAuth2 and
    expired, refresh it. Remember the MCP server captures its environment
    at session start — restart the session after any env change.
- Never commit credentials or tokens to this repository. `.gitignore`
  blocks `.env*`, token directories, and `.claude/settings.local.json`.
