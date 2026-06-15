import streamlit as st
from auth import login

st.set_page_config(
    page_title="AI Loan Approval System",
    page_icon="🏦",
    layout="wide"
)

if not login():
    st.stop()

st.title(
    "🏦 AI Loan Approval & Credit Risk Assessment System"
)

st.markdown(
"""
Welcome to the Loan Analytics Platform.

Use the sidebar to access:

- Dashboard
- Analytics
- Prediction
- History
- Model Insights
"""
)