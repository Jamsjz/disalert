import streamlit as st


def display_home():
    st.title("Disaster Alert App")
    st.write("Welcome to the Disaster Alert App. Please choose an option below.")

    if st.button("Login"):
        st.session_state.page = "login"

    if st.button("Register"):
        st.session_state.page = "register"
