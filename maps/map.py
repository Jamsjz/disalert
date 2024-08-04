import folium
from folium.plugins import MarkerCluster, LocateControl, Fullscreen

def generate_map(alerts_df):
    map_center = [27.7172, 85.3240]
    folium_map = folium.Map(location=map_center, zoom_start=12, tiles="CartoDB positron", zoom_control=False, attribution_control=False)

    # Add satellite layer
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True,
    ).add_to(folium_map)

    # Add location control
    LocateControl(
        position="bottomright",
        auto_start=False,
        ).add_to(folium_map)

   # Add zoom control
    folium.plugins.Fullscreen(
        position='bottomright',
        title='Expand map',
        title_cancel='Exit fullscreen',
        force_separate_button=True
    ).add_to(folium_map)

    # Create a MarkerCluster
    marker_cluster = MarkerCluster().add_to(folium_map)

    # Custom icons for different disaster types
    icons = {
        "Earthquake": "fa-solid fa-house-crack",
        "Flood": "fa-solid fa-water",
        "Fire": "fa-solid fa-fire",
        "Landslide": "fa-solid fa-mountain",
        "Other": "fa-solid fa-triangle-exclamation"
    }

    # Add markers for each alert
    for _, alert in alerts_df.iterrows():
        icon = folium.Icon(color="red", icon=icons.get(alert['type'], "info-sign"), prefix='fa')
        folium.Marker(
            location=[alert["lat"], alert["lon"]],
            popup=f"Type: {alert['type']}<br>Description: {alert['description']}<br>Time: {alert['time']}",
            icon=icon,
        ).add_to(marker_cluster)

    return folium_map
