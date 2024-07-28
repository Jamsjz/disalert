import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
import pytz

# Set page configuration for layout and aesthetics
st.set_page_config(
    page_title="Disaster Alert Map",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# CSS styles for button and layout adjustments
st.markdown(
    """
<style>
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    font-size: 20px;
    border-radius: 10px;
    border: none;
    padding: 15px 30px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    cursor: pointer;
    width: 100%;
}
.center {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    margin-top: -50px;
}
.stDeployButton, .stToolbar, .stDecoration {
    display: none !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# Session state for alerts and map click tracking
if "alerts" not in st.session_state:
    st.session_state.alerts = pd.DataFrame(
        columns=["lat", "lon", "type", "description", "time"]
    )
if "map_click" not in st.session_state:
    st.session_state.map_click = None

# Page title and instructions
st.title("Disaster Alert Map")
st.write(
    "Click on the map to report a disaster. The form will open below with the coordinates filled."
)

if st.button("Emergency", key="emergency-button"):
    lat, lon = 27.7172, 85.3240  # Default location (Kathmandu, Nepal)
    new_alert = pd.DataFrame(
        {
            "lat": [lat],
            "lon": [lon],
            "type": ["Emergency"],
            "description": ["Emergency alert activated!"],
            "time": [
                datetime.now(pytz.timezone("Asia/Kathmandu")).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            ],
        }
    )
    st.session_state.alerts = pd.concat(
        [st.session_state.alerts, new_alert], ignore_index=True
    )
    st.success("Emergency alert reported successfully!")


# Map generation function
def generate_map():
    map_center = [27.7172, 85.3240]
    folium_map = folium.Map(location=map_center, zoom_start=12)
    for _, alert in st.session_state.alerts.iterrows():
        folium.Marker(
            location=[alert["lat"], alert["lon"]],
            popup=f"Type: {alert['type']}<br>Time: {alert['time']}",
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(folium_map)
    return folium_map


# Columns for layout
col1, col2 = st.columns(2)

with col1:
    folium_map = generate_map()
    map_data = st_folium(folium_map, width=1000, height=500)


# Report Details form
with col2:
    st.header("Report Details")
    with st.form(key="alert_form1"):
        alert_type = st.selectbox(
            "Disaster Type", ["Earthquake", "Flood", "Fire", "Landslide", "Other"]
        )
        description = st.text_area("Description (optional)")
        if st.form_submit_button("Submit Alert"):
            new_alert = pd.DataFrame(
                {
                    "lat": 20.593684,
                    "lon": 85.32736,
                    "type": [alert_type],
                    "description": [""],
                    "time": [
                        datetime.now(pytz.timezone("Asia/Kathmandu")).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    ],
                }
            )

    if map_data and map_data["last_clicked"]:
        st.session_state.map_click = map_data["last_clicked"]
        lat, lon = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
        st.session_state.form_lat = lat
        st.session_state.form_lon = lon

    if "form_lat" in st.session_state and "form_lon" in st.session_state:
        lat, lon = st.session_state.form_lat, st.session_state.form_lon
    else:
        lat, lon = None, None

    if lat and lon:
        with st.form(key="alert_form2"):
            st.write(f"Selected Location: {lat:.4f}, {lon:.4f}")
            st.write("Fill out the form and submit the alert.")

            alert_type_input = st.selectbox(
                "Disaster Type",
                ["Earthquake", "Flood", "Fire", "Landslide", "Other"],
                index=["Earthquake", "Flood", "Fire", "Landslide", "Other"].index(
                    alert_type
                ),
            )
            description_input = st.text_area(
                "Description (optional)", value=description
            )

            submitted = st.form_submit_button("Submit Alert")

            if submitted:
                new_alert = pd.DataFrame(
                    {
                        "lat": [lat],
                        "lon": [lon],
                        "type": [alert_type_input],
                        "description": [description_input],
                        "time": [
                            datetime.now(pytz.timezone("Asia/Kathmandu")).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        ],
                    }
                )
                st.session_state.alerts = pd.concat(
                    [st.session_state.alerts, new_alert], ignore_index=True
                )
                st.success("Alert reported successfully!")
                st.session_state.form_lat, st.session_state.form_lon = None, None
                st.experimental_rerun()

# Recent Alerts and Filters
st.header("Recent Alerts")
if not st.session_state.alerts.empty:
    alert_filter_type = st.multiselect(
        "Filter by Type", st.session_state.alerts["type"].unique()
    )
    alert_filter_date = st.date_input("Filter by Date", [])

    filtered_alerts = st.session_state.alerts
    if alert_filter_type:
        filtered_alerts = filtered_alerts[
            filtered_alerts["type"].isin(alert_filter_type)
        ]
    if alert_filter_date:
        filtered_alerts = filtered_alerts[
            filtered_alerts["time"]
            .str[:10]
            .isin([str(date) for date in alert_filter_date])
        ]

    st.dataframe(
        filtered_alerts.sort_values("time", ascending=False).head(5),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.write("No alerts reported yet.")

# Footer information
st.markdown("---")
st.write(
    "This is a crowd-sourced disaster mapping tool. In case of emergency, please contact local authorities."
)
