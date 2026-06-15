import streamlit as st
import pandas as pd
import joblib
import sqlite3
import plotly.graph_objects as go
from datetime import datetime

from utils import generate_report

st.set_page_config(layout="wide")

st.title("🏦 AI Loan Approval Engine")

# -----------------------
# LOAD MODEL
# -----------------------

model = joblib.load("models/best_model.pkl")

# -----------------------
# DATABASE
# -----------------------

conn = sqlite3.connect(
    "database/loan_predictions.db",
    check_same_thread=False
)

# -----------------------
# INPUT FORM
# -----------------------

st.subheader("Applicant Information")

col1, col2 = st.columns(2)

with col1:

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    married = st.selectbox(
        "Married",
        ["Yes", "No"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["0", "1", "2", "3+"]
    )

    education = st.selectbox(
        "Education",
        ["Graduate", "Not Graduate"]
    )

    self_employed = st.selectbox(
        "Self Employed",
        ["Yes", "No"]
    )

with col2:

    applicant_income = st.number_input(
        "Applicant Income",
        min_value=0,
        value=5000
    )

    coapplicant_income = st.number_input(
        "Coapplicant Income",
        min_value=0,
        value=0
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=1,
        value=120
    )

    loan_term = st.number_input(
        "Loan Amount Term",
        min_value=1,
        value=360
    )

    credit_history = st.selectbox(
        "Credit History",
        [1.0, 0.0]
    )

    property_area = st.selectbox(
        "Property Area",
        ["Urban", "Semiurban", "Rural"]
    )

# -----------------------
# PREDICT
# -----------------------

if st.button(
    "🔍 Assess Loan Application",
    use_container_width=True
):

    input_df = pd.DataFrame({

        "Gender":[gender],

        "Married":[married],

        "Dependents":[dependents],

        "Education":[education],

        "Self_Employed":[self_employed],

        "ApplicantIncome":[applicant_income],

        "CoapplicantIncome":[coapplicant_income],

        "LoanAmount":[loan_amount],

        "Loan_Amount_Term":[loan_term],

        "Credit_History":[credit_history],

        "Property_Area":[property_area]
    })

    prediction = model.predict(
        input_df
    )[0]

    probability = max(
        model.predict_proba(
            input_df
        )[0]
    ) * 100

    # -----------------------
    # DECISION
    # -----------------------

    st.divider()

    st.subheader(
        "📋 Assessment Result"
    )

    colA, colB, colC = st.columns(3)

    if prediction == "Y":

        decision = "APPROVED"

        with colA:
            st.success(
                "✅ APPROVED"
            )
    else:

        decision = "REJECTED"

        with colA:
            st.error(
                "❌ REJECTED"
            )

    with colB:

        st.metric(
            "Confidence",
            f"{probability:.2f}%"
        )

    # -----------------------
    # RISK SCORE
    # -----------------------

    risk_score = round(
        100 - probability,
        2
    )
    credit_score = round(probability, 2)

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=credit_score,
            title={"text": "Creditworthiness Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, 40], "color": "red"},
                    {"range": [40, 70], "color": "yellow"},
                    {"range": [70, 100], "color": "green"}
                 ]
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    with colC:

        st.metric(
            "Risk Score",
            f"{risk_score}"
        )

    st.progress(
        int(probability)
    )

    # -----------------------
    # RISK LEVEL
    # -----------------------

    if probability >= 80:

        risk = "🟢 LOW RISK"

    elif probability >= 60:

        risk = "🟡 MEDIUM RISK"

    else:

        risk = "🔴 HIGH RISK"

    st.info(
        f"Risk Category: {risk}"
    )

    # -----------------------
    # DECISION EXPLANATION
    # -----------------------

    st.subheader(
        "🤖 AI Decision Insights"
    )

    positives = []

    risks = []

    if credit_history == 1:
        positives.append(
            "Positive credit history"
        )
    else:
        risks.append(
            "Poor credit history"
        )

    if applicant_income > 5000:
        positives.append(
            "Stable applicant income"
        )

    if loan_amount > 250:
        risks.append(
            "High loan amount"
        )

    if self_employed == "Yes":
        risks.append(
            "Self employed applicant"
        )

    st.write(
        "### Positive Factors"
    )

    for item in positives:
        st.success(item)

    st.write(
        "### Risk Factors"
    )

    if len(risks) == 0:

        st.success(
            "No significant risk factors detected"
        )

    else:

        for item in risks:
            st.warning(item)

    # -----------------------
    # SAVE TO SQLITE
    # -----------------------

    conn.execute(
        """
        INSERT INTO predictions
        (
            timestamp,
            gender,
            married,
            dependents,
            education,
            self_employed,
            applicant_income,
            coapplicant_income,
            loan_amount,
            credit_history,
            property_area,
            prediction,
            probability,
            risk
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            str(datetime.now()),
            gender,
            married,
            dependents,
            education,
            self_employed,
            applicant_income,
            coapplicant_income,
            loan_amount,
            credit_history,
            property_area,
            decision,
            probability,
            risk
        )
    )
    conn.commit()
    st.success(
    "Assessment saved successfully"
)

generate_report(
    "loan_report.pdf",
    decision,
    probability,
    risk,
    applicant_income,
    loan_amount
)

with open(
    "loan_report.pdf",
    "rb"
) as pdf:

    st.download_button(
        "📄 Download PDF Report",
        pdf,
        file_name="Loan_Assessment_Report.pdf",
        mime="application/pdf"
    )

