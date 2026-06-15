import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Prediction History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Loan Assessment History")

# -------------------------
# DATABASE CONNECTION
# -------------------------

conn = sqlite3.connect(
    "database/loan_predictions.db",
    check_same_thread=False
)

# -------------------------
# LOAD DATA
# -------------------------

try:

    history_df = pd.read_sql_query(
        """
        SELECT *
        FROM predictions
        ORDER BY id DESC
        """,
        conn
    )

except:

    history_df = pd.DataFrame()

# -------------------------
# SUMMARY CARDS
# -------------------------

if not history_df.empty:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Assessments",
            len(history_df)
        )

    with col2:

        approved = len(
            history_df[
                history_df["prediction"]
                == "APPROVED"
            ]
        )

        st.metric(
            "Approved",
            approved
        )

    with col3:

        rejected = len(
            history_df[
                history_df["prediction"]
                == "REJECTED"
            ]
        )

        st.metric(
            "Rejected",
            rejected
        )

    with col4:

        avg_conf = round(
            history_df["probability"].mean(),
            2
        )

        st.metric(
            "Avg Confidence",
            f"{avg_conf}%"
        )

st.divider()

# -------------------------
# SEARCH
# -------------------------

st.subheader("🔍 Search Records")

search = st.text_input(
    "Search by Gender, Education, Risk Level"
)

if (
    not history_df.empty
    and search
):

    history_df = history_df[
        history_df.astype(str)
        .apply(
            lambda row:
            row.str.contains(
                search,
                case=False
            ).any(),
            axis=1
        )
    ]

# -------------------------
# FILTERS
# -------------------------

if not history_df.empty:

    col1, col2 = st.columns(2)

    with col1:

        risk_filter = st.selectbox(
            "Filter by Risk",
            ["All"]
            +
            list(
                history_df["risk"]
                .unique()
            )
        )

    with col2:

        prediction_filter = st.selectbox(
            "Filter by Decision",
            ["All"]
            +
            list(
                history_df["prediction"]
                .unique()
            )
        )

    if risk_filter != "All":

        history_df = history_df[
            history_df["risk"]
            == risk_filter
        ]

    if prediction_filter != "All":

        history_df = history_df[
            history_df["prediction"]
            == prediction_filter
        ]

st.divider()

# -------------------------
# TABLE
# -------------------------

st.subheader("📊 Assessment Records")

if history_df.empty:

    st.warning(
        "No assessment records found."
    )

else:

    st.dataframe(
        history_df,
        use_container_width=True
    )

st.divider()

# -------------------------
# DOWNLOAD CSV
# -------------------------

if not history_df.empty:

    csv = history_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇ Download History CSV",
        data=csv,
        file_name="loan_assessment_history.csv",
        mime="text/csv"
    )

st.divider()

# -------------------------
# DELETE ALL RECORDS
# -------------------------

st.subheader("⚠ Database Management")

if st.button(
    "🗑 Delete All Records"
):

    conn.execute(
        "DELETE FROM predictions"
    )

    conn.commit()

    st.success(
        "All records deleted successfully."
    )

    st.rerun()

# -------------------------
# FOOTER
# -------------------------

st.caption(
    "AI-Powered Loan Approval & Credit Risk Assessment System | Developed by Zeelan"
)