import streamlit as st
from api.user import create_user


def handle_register():
    st.title("Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")

    if st.button("Register"):
        if create_user(username, password, email):
            st.success("Registration successful!")
            st.session_state.page = "login"
        else:
            st.error("Registration failed.")
