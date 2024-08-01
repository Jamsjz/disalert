import streamlit as st
from api.user import get_user, verify_user


def handle_login() -> None:
    with st.form("login"):
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.user = get_user(username)
                st.success("Login successful!")
                st.session_state.page = "user_home"
                st.rerun()
            else:
                st.error("Invalid username or password.")
