import folium


def generate_map(alerts_df):
    map_center = [27.7172, 85.3240]
    folium_map = folium.Map(location=map_center, zoom_start=12)

    # Add markers for each alert
    for _, alert in alerts_df.iterrows():
        folium.Marker(
            location=[alert["lat"], alert["lon"]],
            popup=f"Type: {alert['type']}<br>Description: {alert['description']}<br>Time: {alert['time']}",
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(folium_map)

    return folium_map
