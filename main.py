import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime
import pytz

# Set page configuration for mobile responsiveness
st.set_page_config(
    page_title="Disaster Alert Map",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS for the round and big button, and to hide unwanted elements
button_style = """
<style>
.stButton>button {
    background-color: #ff4b4b;
    border: none;
    color: white;
    padding: 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 20px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 50%;
    width: 100px;
    height: 100px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.center {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
}
/* Hide unwanted elements */
.stDeployButton, .stToolbar, .stDecoration {
    display: none !important;
}
</style>
"""

# Display CSS
st.markdown(button_style, unsafe_allow_html=True)

# Initialize session state
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# Create a function to generate a map
def generate_map():
    map_center = [27.7172, 85.3240]  # Kathmandu, Nepal
    folium_map = folium.Map(location=map_center, zoom_start=12)
    
    for alert in st.session_state.alerts:
        folium.Marker(
            [alert['lat'], alert['lon']],
            popup=f"Type: {alert['type']}<br>Time: {alert['time']}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(folium_map)
    
    return folium_map

# Title and instructions
st.title("Disaster Alert Map")
st.write("Click on the map to report a disaster. Use the button below for immediate alerts.")

# Display the map
folium_map = generate_map()
map_data = st_folium(folium_map, width=700, height=500)

# Sidebar for alert details
st.sidebar.header("Report Details")
alert_type = st.sidebar.selectbox("Disaster Type", ["Earthquake", "Flood", "Fire", "Landslide", "Other"])
description = st.sidebar.text_area("Description (optional)")

# Create a form for the alert button
with st.form(key='alert_form'):
    submitted = st.form_submit_button("Alert", use_container_width=True)

# Check if the button was clicked or map was clicked
if submitted or (map_data and map_data['last_clicked']):
    if map_data and map_data['last_clicked']:
        lat, lon = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
    else:
        lat, lon = 27.7172, 85.3240  # Default to map center

    st.session_state.alerts.append({
        'lat': lat,
        'lon': lon,
        'type': alert_type,
        'description': description,
        'time': datetime.now(pytz.timezone('Asia/Kathmandu')).strftime('%Y-%m-%d %H:%M:%S')
    })
    st.warning(f"Alert reported! Type: {alert_type}, Location: {lat:.4f}, {lon:.4f}")
    st.experimental_rerun()

# Display recent alerts
st.header("Recent Alerts")
for alert in reversed(st.session_state.alerts[-5:]):
    st.write(f"Type: {alert['type']}, Time: {alert['time']}, Location: {alert['lat']:.4f}, {alert['lon']:.4f}")
    if alert['description']:
        st.write(f"Description: {alert['description']}")
    st.write("---")

# Add a footer with information
st.markdown("---")
st.write("This is a crowd-sourced disaster mapping tool. In case of emergency, please contact local authorities.")