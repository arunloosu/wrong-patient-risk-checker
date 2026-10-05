# API Documentation

The optional Flask service exposes the same identity-checking logic as the Streamlit UI. It is a prototype API only.

## Base URL
`http://127.0.0.1:5001`

## GET /api/health
Returns service availability.

Example response:
```json
{"status":"ok","service":"wrong-patient-risk-checker"}
```

## POST /api/check
Runs an identity/workflow consistency check.

Request:
```json
{
  "order": {
    "patient_id": "PAT-1001",
    "wristband_id": "WB-1001",
    "dob": "1965-03-12",
    "name": "John A. Miller",
    "location": "Ward-3A Bed-01"
  },
  "scan": {
    "patient_id": "PAT-1003",
    "wristband_id": "WB-1003",
    "dob": "1982-11-05",
    "name": "Maria E. Garcia",
    "location": "Ward-3B Bed-05"
  }
}
```

Response contains `risk_level`, `score`, `human_verification_required`, `discrepancies`, `evidence`, and `check_status`.

## Error boundary
Malformed requests return HTTP 400. Internal failures return HTTP 500 with `fail_closed=true` and `human_verification_required=true`. The API never returns a medicine approval decision.
