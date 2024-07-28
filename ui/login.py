import streamlit as st
from api.user import get_user, verify_password


def handle_login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user(username)
        if user and verify_password(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.session_state.page = "home"
        else:
            st.error("Invalid username or password.")
