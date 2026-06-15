import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Model Insights",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Model Performance & Business Insights")

# -------------------------
# MODEL OVERVIEW
# -------------------------

st.subheader("🤖 Selected Machine Learning Model")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Best Model",
        "Logistic Regression"
    )

with col2:
    st.metric(
        "Accuracy",
        "78.86%"
    )

with col3:
    st.metric(
        "Status",
        "Production Ready"
    )

st.divider()

# -------------------------
# MODEL COMPARISON
# -------------------------

st.subheader("🏆 Model Comparison")

comparison_df = pd.DataFrame({
    "Model": [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest",
        "Gradient Boosting"
    ],
    "Accuracy": [
        78.86,
        71.54,
        77.24,
        77.24
    ]
})

fig = px.bar(
    comparison_df,
    x="Model",
    y="Accuracy",
    text="Accuracy",
    title="Model Accuracy Comparison"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------
# BUSINESS FACTORS
# -------------------------

st.subheader("📈 Important Business Factors")

factor_df = pd.DataFrame({
    "Factor": [
        "Credit History",
        "Applicant Income",
        "Loan Amount",
        "Property Area",
        "Education",
        "Dependents"
    ],
    "Importance": [
        95,
        80,
        72,
        60,
        55,
        40
    ]
})

fig = px.bar(
    factor_df,
    x="Importance",
    y="Factor",
    orientation="h",
    title="Estimated Business Importance"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    """
    Credit History is the strongest indicator of loan approval.
    Applicants with positive credit history are significantly
    more likely to receive approval.
    """
)

st.divider()

# -------------------------
# APPROVAL ANALYSIS
# -------------------------

df = pd.read_csv("loan.csv")

approval_counts = (
    df["Loan_Status"]
    .value_counts()
    .reset_index()
)

approval_counts.columns = [
    "Status",
    "Count"
]

approval_counts["Status"] = (
    approval_counts["Status"]
    .replace({
        "Y": "Approved",
        "N": "Rejected"
    })
)

fig = px.pie(
    approval_counts,
    names="Status",
    values="Count",
    title="Loan Approval Breakdown"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------
# EXECUTIVE SUMMARY
# -------------------------

st.subheader("📋 Executive Summary")

st.success(
    """
    Model Performance: GOOD

    • Logistic Regression achieved the highest accuracy.

    • Credit History is the strongest factor.

    • Majority of applicants are approved.

    • The system can be used as a decision-support tool
      for preliminary loan assessment.
    """
)

st.divider()

# -------------------------
# RECRUITER SECTION
# -------------------------

st.subheader("💼 Project Highlights")

st.markdown("""
### Technologies Used

- Python
- Pandas
- Scikit-Learn
- Streamlit
- Plotly
- SQLite

### Features Implemented

✅ Data Preprocessing

✅ Model Training

✅ Model Evaluation

✅ Risk Assessment

✅ Loan Prediction

✅ Interactive Analytics

✅ SQLite Database Storage

✅ Multi-Page Streamlit Application

✅ Business Intelligence Dashboard

### Use Case

Financial institutions can use this system
for preliminary loan eligibility assessment
and credit risk evaluation.
""")

st.caption(
    "AI-Powered Loan Approval & Credit Risk Assessment System | Developed by Zeelan"
)