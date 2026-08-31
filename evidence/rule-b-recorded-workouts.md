# Rule B — deliberately recorded sessions → routed per channel

Rule B routes **two channels separately**, and they do not share a status.
Scope was refined on 2026-08-30 into the channel split after a ring-class
device in the reference configuration shipped session recording with external
strap support; see "Scope" below.

| Channel | Routing basis | Measurement confidence |
|---|---|---|
| `event` — GPS, pace, distance, duration, power, cadence, load | **`structural`** — usually only one overlapping record carries these at all; when two do, a `tiebreaks.recorded_workout` entry resolves it and the basis becomes `user_preference` | `high` — nothing in the evidence challenges event data from a recorder |
| `heart_rate` — in-workout HR | **`evidence_backed`** (2026-07-14, refined 2026-08-30) — the placement hierarchy is cited and multi-brand | **Depends on the sensor class present and on intensity**, not on the rule: `high` with an external monitor, `low` for wrist optical at effort, `unvalidated` for ring PPG, `unusable` in water |

Both dimensions are defined in
[`../spec/routed-observation.md`](../spec/routed-observation.md). One open gap
remains, for sessions with no external monitor.

## Claim

For a session actively recorded on a device built for it, the recording is the
governing source for the event — pace, distance, power, cadence, training load
— over any other device's estimate of the same event. The heart rate of that
same session is a separate claim, routed by sensor class rather than by which
device recorded it.

## Evidence

The HR trust hierarchy and all four supporting studies now live in
**[`general/hr-sensor-placement.md`](general/hr-sensor-placement.md)** —
Etiwy 2019, Pasadyn 2019, Hettiarachchi 2019 and Schweizer &
Gilgen-Ammann 2025. It is device-agnostic: sensing method and anatomical
placement determine accuracy, not brand.

Device-specific figures (e.g. which watch model measured rc=0.52) are in
[`devices/garmin.md`](devices/garmin.md), and do not transfer to another
device.

## Why this is generation-robust

The failure mode is physical, not firmware: optical PPG at the wrist is
corrupted by motion artifact and perfusion changes during exercise, while a
chest strap reads the ECG signal directly. That relationship does not change
across device generations, so — unlike Rule A — this rule does not hinge on
which specific model is paired.

## Scope: two channels, routed separately

Updated 2026-08-30. The evidence supports a **channel split**, not a
single per-record winner. The event and the heart rate are different claims
with different sensors behind them.

- **EVENT channel** (GPS, pace, distance, duration, power, cadence, training
  load): the richer recorder wins, always. Fully supported — this is the only
  device that captured the session at all.
- **HR channel**: routed by **sensor class, not by brand and not by which app
  recorded the session.** The strap is the sensor; the watch or phone is only
  the recorder.

See **[`general/hr-sensor-placement.md`](general/hr-sensor-placement.md)**
for the full five-class hierarchy with its citations. In short:
`ecg_chest_strap` (highest) and `optical_armband` (high) together form the
routing class **`external_hr_monitor`**, which beats `wrist_optical` (low
during exercise) and `ring_ppg` (unvalidated during exercise).

**Placement is the variable, not brand.** Every reference-grade measurement
came from a Polar device paired into non-Polar setups, and the armband/wrist
split in Schweizer & Gilgen-Ammann is *within a single brand* — same protocol,
same criterion, arm beat wrist ~4.5× on MAE.

**Two caveats that survive the good armband numbers:** optical armbands lag
during rapid HR transitions (intervals, sprint starts), and they are
placement-sensitive. For interval work a chest strap remains preferable. This
is why the two subtypes are ranked rather than treated as interchangeable.

## Open gap — sessions with no external HR monitor

When no external monitor (strap or armband) is present, the choice is
between a **known-bad** number
(wrist optical, rc≈0.52) and an **unvalidated** one (ring PPG). There is no
study comparing ring PPG against ECG *during exercise*, so the ring cannot be
promoted on evidence.

The rule therefore keeps the recording device's HR and requires an explicit
low-confidence flag. It does **not** hand HR to the ring. Swapping a
measured-poor value for an unmeasured one would look like an upgrade while
removing the ability to say how wrong it is.

**Closes when:** an independent ECG-referenced comparison of ring PPG during
exercise exists. Until then this is stated as a gap, not resolved by
preference.

## Detectability caveat (implementation, not evidence)

Neither API exposes which HR sensor fed a session. Garmin's
`device_manufacturer` names the **recorder**, not the sensor. Running dynamics
(ground contact time, vertical oscillation) are **not** a usable strap proxy on
watches that produce them from the wrist — the Forerunner 955 does. External-monitor use
must therefore be **declared by the user**, and undeclared sessions must be
treated as unmonitored for confidence purposes rather than assumed either way.
