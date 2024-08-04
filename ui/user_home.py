import streamlit as st
from api.user import get_user
from ui.alert import create_alert, edit_alert, delete_alert, all_alerts
from ui.map import map_view
from ui.settings import settings


def sidebar():
    # Sidebar Title
    st.sidebar.title("Navigation")

    # My Alerts Section
    st.sidebar.subheader("My Alerts")
    create_alert = st.sidebar.button("Create Alert")
    edit_alert = st.sidebar.button("Edit Alert")
    delete_alert = st.sidebar.button("Delete Alert")

    # All Alerts Section
    all_alerts = st.sidebar.button("All Alerts")

    # Map Section
    map_view = st.sidebar.button("Map")

    # Settings Section
    settings = st.sidebar.button("Settings")

    if st.sidebar.button(":red[Logout]"):
        return "logout"

    # Return the chosen option
    if create_alert:
        return "create_alert"
    elif edit_alert:
        return "edit_alert"
    elif delete_alert:
        return "delete_alert"
    elif all_alerts:
        return "all_alerts"
    elif map_view:
        return "map"
    elif settings:
        return "settings"
    else:
        return None


def logout():
    from ui.home import display_home

    st.session_state.clear()
    st.rerun()

    display_home()


def create_sidebar(placeholder):
    choice = sidebar()

    if choice == "create_alert":
        create_alert()
    elif choice == "edit_alert":
        edit_alert()
        # Add code to handle alert editing
    elif choice == "delete_alert":
        delete_alert()
        # Add code to handle alert deletion
    elif choice == "all_alerts":
        all_alerts()
        # Add code to display all alerts
    elif choice == "map":
        map_view()
        # Add code to display map
    elif choice == "settings":
        settings()
    elif choice == "logout":
        placeholder.empty()
        logout()


def user_by_username():
    user = get_user(st.session_state.user.username)
    if user is None:
        logout()
        st.rerun()
    return user


def user_home():
    user = user_by_username()
    placeholder = st.empty()
    create_sidebar(placeholder)
    with placeholder.container():
        st.title(f"Welcome {user.username}")
        st.write(f"Email: {user.email}")
