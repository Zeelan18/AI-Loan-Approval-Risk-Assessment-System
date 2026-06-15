import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📈 Advanced Loan Analytics")

df = pd.read_csv("loan.csv")

# Sidebar Filters

st.sidebar.header("Filters")

selected_area = st.sidebar.multiselect(
    "Property Area",
    df["Property_Area"].unique(),
    default=df["Property_Area"].unique()
)

selected_education = st.sidebar.multiselect(
    "Education",
    df["Education"].unique(),
    default=df["Education"].unique()
)

filtered_df = df[
    (df["Property_Area"].isin(selected_area))
    &
    (df["Education"].isin(selected_education))
]

st.success(
    f"Showing {len(filtered_df)} records"
)

# -------------------
# Row 1
# -------------------

col1, col2 = st.columns(2)

with col1:

    approval_data = (
        filtered_df["Loan_Status"]
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
        title="Approval vs Rejection"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.histogram(
        filtered_df,
        x="ApplicantIncome",
        nbins=40,
        title="Income Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------
# Row 2
# -------------------

col3, col4 = st.columns(2)

with col3:

    property_analysis = (
        filtered_df.groupby(
            "Property_Area"
        )["Loan_Status"]
        .count()
        .reset_index()
    )

    fig = px.bar(
        property_analysis,
        x="Property_Area",
        y="Loan_Status",
        title="Applications by Area"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col4:

    education_analysis = (
        filtered_df.groupby(
            "Education"
        )["Loan_Status"]
        .count()
        .reset_index()
    )

    fig = px.bar(
        education_analysis,
        x="Education",
        y="Loan_Status",
        title="Applications by Education"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------
# Row 3
# -------------------

st.subheader("💰 Income vs Loan Amount")

fig = px.scatter(
    filtered_df,
    x="ApplicantIncome",
    y="LoanAmount",
    color="Loan_Status",
    title="Income vs Loan Amount"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------
# Correlation
# -------------------

st.subheader("📊 Numerical Correlation")

corr_cols = [
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Credit_History"
]

corr = filtered_df[corr_cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    title="Correlation Heatmap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)