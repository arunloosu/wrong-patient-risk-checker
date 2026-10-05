# User Guide

1. Install dependencies with `python -m pip install -r requirements.txt`.
2. Run `streamlit run src/app.py`.
3. Enter the intended patient/order identifiers and bedside scan identifiers.
4. Click **Run Safety Check**.
5. Review risk level, verification score, discrepancies, and evidence.
6. For MEDIUM/HIGH or missing data, perform human verification before any action.
7. The prototype never provides a medicine approval decision.

For automated validation run `python src/evaluate.py` and `python -m unittest discover -s tests -v`.
