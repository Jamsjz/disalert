import streamlit as st
from ui.home import display_home
from ui.login import handle_login
from ui.register import handle_register


def main():
    st.set_page_config(page_title="Disaster Alert App", page_icon="🚨", layout="wide")

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        display_home()
    elif st.session_state.page == "login":
        handle_login()
    elif st.session_state.page == "register":
        handle_register()


if __name__ == "__main__":
    main()
