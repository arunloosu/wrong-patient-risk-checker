# Patient Journey Demonstrations

## Journey 1 — STAT / High Urgency
A STAT order for PAT-1001 is followed by a bedside scan for a different patient/wristband. Patient ID and wristband mismatches trigger a deterministic HIGH-risk hard stop. The output provides evidence and requires human verification. No medicine approval or treatment decision is made.

## Journey 2 — Routine / Location Discrepancy
A routine order for PAT-1008 has matching identity identifiers, but the scan location differs from the registered ward/bed. The system produces MEDIUM risk and requests human verification of the current location/context.
