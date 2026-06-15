import streamlit as st

def login():

    # Session State
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Already Logged In
    if st.session_state.logged_in:
        return True

    # -----------------------------
    # PAGE HEADER
    # -----------------------------

    st.title("🏦 AI-Powered Loan Approval & Credit Risk Assessment System")

    st.markdown("""
    ### Secure Login Portal

    Welcome to the Banking Analytics Platform.

    Please login to access:

    - 📊 Executive Dashboard
    - 📈 Advanced Analytics
    - 🤖 Loan Approval Prediction
    - 📜 Assessment History
    - 📊 Model Insights
    - 📄 PDF Assessment Reports
    """)

    st.divider()

    # -----------------------------
    # LOGIN FORM
    # -----------------------------

    username = st.text_input(
        "👤 Username"
    )

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    if st.button(
        "🔐 Login",
        use_container_width=True
    ):

        if (
            username == "admin"
            and
            password == "admin123"
        ):

            st.session_state.logged_in = True

            st.success(
                "✅ Login Successful"
            )

            st.rerun()

        else:

            st.error(
                "❌ Invalid Username or Password"
            )

    st.divider()

    # -----------------------------
    # DEMO CREDENTIALS
    # -----------------------------

    st.subheader(
        "🎓 Project Demonstration Credentials"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Username**")
        st.code("admin")

    with col2:
        st.write("**Password**")
        st.code("admin123")

    
    

    return False