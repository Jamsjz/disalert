import streamlit as st
import pandas as pd
from ui.home import display_home
from ui.login import handle_login
from ui.register import handle_register


def main():

    # Set page configuration
    st.set_page_config(
        layout="wide",
        page_title="Disaster Alert App",
        page_icon="🚨",
        )

    # Load CSS and JS files
    load_css("ui/styles.css")
    load_js("ui/scripts.js")

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if "alerts" not in st.session_state:
        st.session_state.alerts = pd.DataFrame(columns=["lat", "lon", "type", "description", "time"])

    if st.session_state.page == "home":
        display_home()
    elif st.session_state.page == "login":
        handle_login()
    elif st.session_state.page == "register":
        handle_register()

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_js(file_name):
    with open(file_name) as f:
        st.markdown(f'<script>{f.read()}</script>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
