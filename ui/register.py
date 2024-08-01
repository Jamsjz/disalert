import streamlit as st
from api.user import create_user, check_username
from api.verification import is_valid_email, is_valid_password


def check_valid_registration(username, password, email):
    if username is not None:
        is_valid_username = check_username(username)
        if not is_valid_username:
            st.error("Username already taken.", icon="❌")
            return False

    if password is not None:
        if not is_valid_password(password):
            return False

    if email is not None:
        if not is_valid_email(email):
            st.error("Invalid email address.", icon="❌")
            return False

    return True if all([username, password, email]) else False


def submitted(email, password, username):
    if not check_valid_registration(username, password, email):
        st.write("Details invalid.")
        return
    st.session_state.user = create_user(username, password, email)
    if st.session_state.user is not None:
        st.success("Registration successful!")
    else:
        st.error("Registration failed.")
    st.session_state.page = "login"
    st.rerun()


def handle_register():
    with st.form("register"):
        st.title("Register")

        username = st.text_input("Username", value=None)

        password = st.text_input("Password", type="password", value=None)

        email = st.text_input("Email", value=None)

        if st.form_submit_button("Register"):
            submitted(email, password, username)
