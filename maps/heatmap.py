import folium
from folium.plugins import HeatMap
import pandas as pd


def generate_heatmap(alerts_df):
    map_center = [27.7172, 85.3240]
    folium_map = folium.Map(location=map_center, zoom_start=12)

    # Different colors for different types of disasters
    type_colors = {
        "Earthquake": "red",
        "Flood": "blue",
        "Fire": "orange",
        "Landslide": "green",
        "Other": "purple",
    }

    for _, alert in alerts_df.iterrows():
        folium.CircleMarker(
            location=[alert["lat"], alert["lon"]],
            radius=8,
            color=type_colors.get(alert["type"], "gray"),
            fill=True,
            fill_color=type_colors.get(alert["type"], "gray"),
            fill_opacity=0.7,
            popup=f"Type: {alert['type']}<br>Description: {alert['description']}<br>Time: {alert['time']}",
        ).add_to(folium_map)

    return folium_map
