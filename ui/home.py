import streamlit as st
from streamlit_folium import st_folium
from maps.map  import generate_map
from maps.heatmap import generate_heatmap
from datetime import datetime
import pytz
import pandas as pd


def display_home():
    st.markdown("""
        <div class="map-title">
            <h1>Alert Map</h1>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("Alert Controls")

    if st.sidebar.button("🚨 Emergency", key="emergency-button", help="Click to report an emergency"):
        lat, lon = 27.7172, 85.3240  # Default location (Kathmandu, Nepal)
        new_alert = pd.DataFrame({
            "lat": [lat],
            "lon": [lon],
            "type": ["Emergency"],
            "description": ["Emergency alert activated!"],
            "time": [datetime.now(pytz.timezone("Asia/Kathmandu")).strftime("%Y-%m-%d %H:%M:%S")]
        })
        st.session_state.alerts = pd.concat([st.session_state.alerts, new_alert], ignore_index=True)
        st.sidebar.success("Emergency alert reported successfully!")

    map_type = st.sidebar.radio("Select Map Type", ["Standard", "Heatmap"])

    disaster_types = st.sidebar.multiselect(
        "Filter by Disaster Type",
        ["Earthquake", "Flood", "Fire", "Landslide", "Other"],
        default=["Earthquake", "Flood", "Fire", "Landslide", "Other"]
    )

    date_range = st.sidebar.date_input("Select Date Range", [])

    filtered_alerts = st.session_state.alerts[
        (st.session_state.alerts['type'].isin(disaster_types)) &
        (st.session_state.alerts['time'].dt.date.between(*date_range) if len(date_range) == 2 else True)
    ]

    if map_type == "Standard":
        folium_map = generate_map(filtered_alerts)
    else:
        folium_map = generate_heatmap(filtered_alerts)

    st_folium(folium_map, width="100%")

    # Display recent alerts
    st.markdown('<div class="recent-alerts-card">', unsafe_allow_html=True)
    st.markdown("### Recent Alerts")
    for _, alert in st.session_state.alerts.tail(5).iterrows():
        st.markdown(f"**{alert['time']}** - {alert['type']}: {alert['description']}")
    st.markdown('</div>', unsafe_allow_html=True)


        
    # Add footer with artifacts
    st.markdown('<div class="footer-artifacts"></div>', unsafe_allow_html=True)
