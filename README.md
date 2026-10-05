# Wrong-Patient Risk Checker Using Multiple Identifiers

## Review 2 — Advanced Working MVP / 80% Stage

A synthetic, explainable safety prototype for detecting possible wrong-patient selection before high-risk medicine administration in a busy inpatient ward.

### Safety boundary
This project only checks identity/workflow consistency. It does **not** diagnose, prescribe, dose, administer, approve, reject, substitute, or modify treatment. Human verification remains the final control.

## Implemented
- 20 synthetic patients, 30 orders, 30 wristband scans, 20 benchmark cases.
- Patient ID, wristband ID, DOB, name and location comparison.
- Weighted scoring and LOW/MEDIUM/HIGH classification.
- Deterministic hard stops for critical ID/wristband mismatch.
- Missing-data fail-closed behavior.
- Fuzzy name similarity using Jaro-Winkler/Levenshtein/Soundex support.
- Explainable evidence and audit output.
- Baseline and multi-identifier evaluation.
- Precision, recall, F1, FP/FN and latency metrics.
- STAT and routine patient journeys.
- Edge/failure handling and automated unit tests.
- Optional Flask API and documented endpoints.
- Database-ready schema documentation while keeping the MVP CSV-based.
- Streamlit UI and reproducible evaluation.

## Review 2 validation
- Benchmark: 20/20 PASS.
- Fuzzy name tests: 10/10 PASS.
- Safety unit tests: 8/8 PASS.
- Current synthetic benchmark: 100% accuracy/precision/recall, 0 FP, 0 FN.
- Mean benchmark latency is reported by `src/evaluate.py`.

These are synthetic prototype results, not a clinical safety guarantee.

## Run the project
```bash
python -m pip install -r requirements.txt
python src/evaluate.py
python -m unittest discover -s tests -v
streamlit run src/app.py
```

Optional API:
```bash
python src/api.py
```
Then use `GET /api/health` and `POST /api/check`. See `docs/api.md`.

## Repository structure
```text
data/       synthetic CSV datasets
docs/        architecture, journeys, API, schema, tests and safety docs
outputs/     evaluation JSON
src/         checker, evaluation, UI and API
tests/       automated unit/safety tests
config.json  configurable weights and thresholds
```

## Data / database schema
The MVP uses CSV files to avoid an external database dependency. The relational mapping and future SQLite/PostgreSQL migration plan are documented in `docs/database_schema.md`.

## Error boundaries
The project follows a fail-closed rule: missing critical data, invalid input, or service errors must never be interpreted as a LOW-risk match. See `docs/error_boundaries.md` and `docs/unit_testing.md`.

## Review 2 feedback addressed
- Granular unit-testing documentation added.
- Error boundaries and fail-closed behavior documented and implemented.
- Code comments/docstrings added around safety-critical logic.
- API endpoints documented and implemented.
- Database/data schema documented.
- README expanded with setup, testing, API, schema and safety information.

## Limitations
All patient and clinical information is synthetic. The prototype has not been clinically validated and must not be used to make real-world medicine administration decisions.
