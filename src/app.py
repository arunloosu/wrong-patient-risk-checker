"""Streamlit demo UI for the safety-bounded checker."""
import json
import streamlit as st
from checker import safe_check

st.set_page_config(page_title="Wrong-Patient Risk Checker", layout="wide")

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

st.title("Wrong-Patient Risk Checker")
st.caption("Synthetic prototype only — identity/workflow consistency checking; human verification remains mandatory.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Medicine Order / Intended Patient")
    order = {
        "patient_id": st.text_input("Patient ID", "PAT-1001"),
        "wristband_id": st.text_input("Expected Wristband ID", "WB-1001"),
        "dob": st.text_input("DOB", "1965-03-12"),
        "name": st.text_input("Legal Name", "John A. Miller"),
        "location": st.text_input("Registered Ward/Bed", "Ward-3A, Bed-01"),
    }
with col2:
    st.subheader("Bedside Scan")
    scan = {
        "patient_id": st.text_input("Scanned Patient ID", "PAT-1001"),
        "wristband_id": st.text_input("Scanned Wristband ID", "WB-1001"),
        "dob": st.text_input("Resolved DOB", "1965-03-12"),
        "name": st.text_input("Resolved Legal Name", "John A. Miller"),
        "location": st.text_input("Actual Scan Location", "Ward-3A, Bed-01"),
    }

if st.button("Run Safety Check", type="primary"):
    result = safe_check(order, scan, config)
    if result.risk_level == "LOW":
        st.success("LOW RISK — IDENTIFIERS MATCH")
    elif result.risk_level == "MEDIUM":
        st.warning("MEDIUM RISK — HUMAN VERIFICATION REQUIRED")
    else:
        st.error("HIGH RISK — HUMAN VERIFICATION REQUIRED")

    a, b, c = st.columns(3)
    a.metric("Risk", result.risk_level)
    b.metric("Verification Score", f"{result.score}/100")
    c.metric("Additional Escalation", "NO" if result.risk_level == "LOW" else "YES")

    st.info("Human Final Verification: REQUIRED\n\nAutomatic Medicine Approval: NOT ALLOWED")
    st.write("### Discrepancies")
    st.write(result.discrepancies or ["None"])
    st.write("### Evidence / Audit Output")
    for item in result.evidence:
        st.write("•", item)
