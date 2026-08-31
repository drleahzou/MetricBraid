# Device dossier — <DEVICE NAME>

<!--
Copy this file to evidence/devices/<device>.md when adding a device.
A dossier is not required to USE a device — routing works from capability
classes alone. A dossier is required to make ACCURACY claims about it.

Rules for filling this in:
  - Every row must have been read against the primary source. Never cite from
    memory, and never from a search summary or an abstract alone.
  - Source-quality bar, in order:
      1. Peer-reviewed validation vs a clinical reference (PSG for sleep,
         ECG for HR/HRV)
      2. Independent testers who publish their reference-device methodology
      3. NEVER vendor marketing, spec sheets, or press coverage
  - Record the device GENERATION. A 2019 finding may describe hardware nobody
    wears now.
  - Record conflicts of interest, including manufacturer-supplied hardware
    or data.
  - Say what the evidence does NOT establish. That section is not optional —
    it is the most useful part of every dossier in this repo.
-->

**Device-specific. These numbers do NOT transfer to other devices.** For
baselines applying to any consumer wearable, see [`../general/`](../general/).

Declared capabilities: `<passive_247 | recorded_workout | auto_detected>`.
HR sensor: `<ecg_chest_strap | optical_armband | wrist_optical | ring_ppg>`.

**A dossier grades measurements, not routing.** The confidence column below is
`measurement_confidence` — `high | moderate | low | unvalidated | unusable`,
defined in [`../routed-observation.md`](../routed-observation.md).
Nothing you write here changes a rule's `routing_basis`: capability classes
decide which source owns a signal, and evidence decides what that source's
number is worth. Adding a dossier for a device does not promote it over
another device.

## Evidence

| Date read | Source (journal, PMC/DOI links) | Methodology & reference standard | Generation | Measurement confidence | Findings |
|---|---|---|---|---|---|
| YYYY-MM-DD | | | | | |

## What these numbers oblige

- <what may now be said, and how confidently — per signal, since one device
  can be `high` on duration and `low` on staging>

## What this evidence does NOT establish

- <the gaps — be specific. Which metrics are uncited? Which generation is
  untested? What comparison was never made?>

## Uncited sub-signals

- <metrics the device reports that have no validation at all>
