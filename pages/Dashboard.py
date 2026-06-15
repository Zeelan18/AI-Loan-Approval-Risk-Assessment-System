import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Load dataset
df = pd.read_csv("loan.csv")

st.title("📊 Executive Dashboard")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

total_apps = len(df)
approval_rate = round((df["Loan_Status"] == "Y").mean() * 100, 2)
avg_income = int(df["ApplicantIncome"].mean())
avg_loan = int(df["LoanAmount"].fillna(df["LoanAmount"].median()).mean())

with col1:
    st.metric("Total Applications", total_apps)

with col2:
    st.metric("Approval Rate", f"{approval_rate}%")

with col3:
    st.metric("Average Income", f"₹{avg_income:,}")

with col4:
    st.metric("Average Loan", f"₹{avg_loan:,}")

st.divider()

# Charts
col1, col2 = st.columns(2)

with col1:

    approval_data = (
        df["Loan_Status"]
        .value_counts()
        .reset_index()
    )

    approval_data.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        approval_data,
        names="Status",
        values="Count",
        title="Loan Approval Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.histogram(
        df,
        x="ApplicantIncome",
        nbins=30,
        title="Applicant Income Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# Property Area Analysis

property_data = (
    df.groupby(
        "Property_Area"
    )["Loan_Status"]
    .count()
    .reset_index()
)

fig = px.bar(
    property_data,
    x="Property_Area",
    y="Loan_Status",
    title="Applications by Property Area"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Dataset Preview

st.subheader("Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)