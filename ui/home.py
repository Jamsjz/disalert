import streamlit as st
from ui.login import handle_login
from ui.register import handle_register
from ui.user_home import user_home


def display_home():
    st.title("Disaster Alert App")

    choice = st.selectbox("Login/Register", ["Login", "Register"])
    if "user" in st.session_state and st.session_state.user is not None:
        username = st.session_state.user.username
        st.write("Welcome back, {}!".format(username))
        user_home()

    if choice == "Login":
        handle_login()

    if choice == "Register":
        handle_register()
