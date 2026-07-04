import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
from database import create_user, verify_user

def render():
    if st.button("← Back to Home"):
        st.session_state.view = "landing"
        st.rerun()

    st.markdown('<div class="section-header">Welcome to AutoInsight</div>', unsafe_allow_html=True)
    st.caption("Upload data. Get instant insight. Ask questions. Export reports.")

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Log In")

            if submitted:
                if not username or not password:
                    st.error("Please enter both username and password.")
                else:
                    success, result = verify_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_id = result
                        st.session_state.username = username
                        st.session_state.view = "app"
                        st.rerun()
                    else:
                        st.error(result)

    with tab_signup:
        with st.form("signup_form"):
            new_username = st.text_input("Choose a username", key="signup_username")
            new_password = st.text_input("Choose a password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm password", type="password", key="signup_confirm")
            submitted = st.form_submit_button("Create Account")

            if submitted:
                if not new_username or not new_password:
                    st.error("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    success, msg = create_user(new_username, new_password)
                    if success:
                        st.success(msg + " Please log in.")
                    else:
                        st.error(msg)