# Database / Data Schema

The MVP uses CSV files so it can run without an external database. The schema is intentionally database-ready for later migration to SQLite/PostgreSQL.

## patients
- patient_id: unique patient identifier (text)
- name: legal name (text)
- dob: date of birth (ISO date)
- location: registered ward/bed (text)
- wristband_id: wristband identifier (text)

## orders
- order_id: unique order identifier
- patient_id: intended patient identifier
- name: intended legal name
- dob: intended date of birth
- location: registered ward/bed
- wristband_id: expected wristband
- medicine: synthetic medicine label
- urgency: Routine or STAT

## wristband_scans
- scan_id: unique scan event identifier
- patient_id: scanned patient identifier
- name: resolved name
- dob: resolved date of birth
- location: scan location
- wristband_id: scanned wristband identifier

## test_cases
- case_id: benchmark case identifier
- order_id: referenced order
- scan_id: referenced scan
- expected_risk: expected LOW/MEDIUM/HIGH outcome

## Future relational mapping
`patients (1) -> (many) orders`
`patients (1) -> (many) wristband_scans`
`orders + wristband_scans -> test_cases`

No real patient/clinical data is used by this repository.
