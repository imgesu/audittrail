import streamlit as st
import pandas as pd
from scoring import risk_score_audit_trail
from pdf_export import export_audit_pdf

import streamlit as st

# Basic password protection
st.title("🔐 Login Required")

password = st.text_input("Enter password", type="password")
if password != "gxpsecure123":
    st.warning("🔒 Access denied. Please enter the correct password.")
    st.stop()


st.set_page_config(page_title="Audit Trail Risk Analyzer")
st.title("🔍 Audit Trail Risk Analyzer – GxP AI SaaS MVP")

uploaded_file = st.file_uploader("📤 Upload Audit Trail CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    result = risk_score_audit_trail(df)

    st.subheader("📊 Risk Analysis")
    st.dataframe(result)

    high_risk = result[result["Risk_Score"] > 0]
    st.subheader("⚠️ High-Risk Events Only")
    st.dataframe(high_risk)

    csv = high_risk.to_csv(index=False).encode("utf-8")
    st.download_button("Download High-Risk Report (CSV)", csv, "high_risk_audit_log.csv", "text/csv")

    pdf_path = export_audit_pdf(high_risk)
    with open(pdf_path, "rb") as pdf_file:
        st.download_button("Download High-Risk Report (PDF)", pdf_file, "audit_risk_report.pdf", "application/pdf")
else:
    st.info("Upload a CSV with columns: Record_ID, Timestamp, User, Action, System")
