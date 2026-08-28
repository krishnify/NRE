"""
Reusable interactive map component using Folium.
Supports: satellite view, click-to-pin location, draggable marker, geocoder search.
"""

import folium
import folium.plugins
from streamlit_folium import st_folium
import streamlit as st
from utils.helpers import format_price, property_icon, AREA_COORDS, NELLORE_LAT, NELLORE_LON


# ── Tile layer definitions ────────────────────────────────────────────────────

SATELLITE_TILES = (
    "https://server.arcgisonline.com/ArcGIS/rest/services/"
    "World_Imagery/MapServer/tile/{z}/{y}/{x}"
)
SATELLITE_ATTR = (
    "Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics, "
    "and the GIS User Community"
)

HYBRID_LABELS_TILES = (
    "https://server.arcgisonline.com/ArcGIS/rest/services/"
    "Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}"
)


def make_folium_map(
    lat: float,
    lon: float,
    zoom: int = 15,
    height: int = 430,
    marker_popup: str = "Property Location",
    show_click_hint: bool = True,
) -> dict:
    """
    Render an interactive Folium map with satellite + street layers and search plugin.
    Clicking on the map returns the clicked coordinates.
    """

    # ── Build map ──────────────────────────────────────────────────────────────
    m = folium.Map(
        location=[lat, lon],
        zoom_start=zoom,
        tiles=None,
        prefer_canvas=True,
    )

    # ── Satellite layer (default) ──────────────────────────────────────────────
    folium.TileLayer(
        tiles=SATELLITE_TILES,
        attr=SATELLITE_ATTR,
        name="🛰️ Satellite",
        overlay=False,
        control=True,
    ).add_to(m)

    # ── Hybrid: satellite + place-name labels ─────────────────────────────────
    folium.TileLayer(
        tiles=HYBRID_LABELS_TILES,
        attr="Esri",
        name="🛰️ Satellite + Labels",
        overlay=True,
        control=True,
        opacity=1,
    ).add_to(m)

    # ── Street map layer ───────────────────────────────────────────────────────
    folium.TileLayer(
        tiles="OpenStreetMap",
        name="🗺️ Street Map",
        overlay=False,
        control=True,
    ).add_to(m)

    # ── Marker at current position ─────────────────────────────────────────────
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(marker_popup, max_width=220),
        tooltip="📍 " + marker_popup,
        icon=folium.Icon(color="red", icon="home", prefix="fa"),
    ).add_to(m)

    # ── Crosshair circle at marker ─────────────────────────────────────────────
    folium.CircleMarker(
        location=[lat, lon],
        radius=8,
        color="#FF6B00",
        fill=True,
        fill_color="#FF6B00",
        fill_opacity=0.25,
        tooltip="Click anywhere on the map to move the pin",
    ).add_to(m)

    # ── In-map Geocoder Search Tool ──────────────────────────────────────────
    try:
        folium.plugins.Geocoder(position="topleft", add_marker=False, collapsed=True).add_to(m)
    except Exception:
        pass

    # ── Layer switcher (top-right) ─────────────────────────────────────────────
    folium.LayerControl(position="topright", collapsed=False).add_to(m)

    # ── Render ─────────────────────────────────────────────────────────────────
    if show_click_hint:
        st.caption(
            "🖱️ **Click anywhere on the map** to pin your property location. "
            "Use the layer switcher (top-right) to switch between Satellite and Street view."
        )

    map_data = st_folium(
        m,
        use_container_width=True,
        height=height,
        returned_objects=["last_clicked"],
    )

    return map_data


def properties_overview_map(properties: list[dict], height: int = 380) -> None:
    """
    Show multiple properties as markers on a satellite map (Browse page).
    """
    if not properties:
        return

    # Centre on average of all property coords
    lats = [p["latitude"] for p in properties]
    lons = [p["longitude"] for p in properties]
    centre_lat = sum(lats) / len(lats)
    centre_lon = sum(lons) / len(lons)

    m = folium.Map(
        location=[centre_lat, centre_lon],
        zoom_start=12,
        tiles=None,
        prefer_canvas=True,
    )

    # Satellite default
    folium.TileLayer(
        tiles=SATELLITE_TILES,
        attr=SATELLITE_ATTR,
        name="🛰️ Satellite",
        overlay=False,
        control=True,
    ).add_to(m)

    # Labels overlay
    folium.TileLayer(
        tiles=HYBRID_LABELS_TILES,
        attr="Esri",
        name="🛰️ Satellite + Labels",
        overlay=True,
        control=True,
    ).add_to(m)

    folium.TileLayer("OpenStreetMap", name="🗺️ Street Map", overlay=False, control=True).add_to(m)

    # Add a marker for each property
    for prop in properties:
        icon_text = property_icon(prop["property_type"])
        price_str = format_price(prop["price"])
        popup_html = f"""
        <div style="font-family:sans-serif;min-width:160px;">
            <b>{prop['title']}</b><br>
            📍 {prop['locality']}<br>
            💰 <b>{price_str}</b><br>
            🏠 {prop['property_type']}
        </div>
        """
        folium.Marker(
            location=[prop["latitude"], prop["longitude"]],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=f"{icon_text} {prop['locality']} — {price_str}",
            icon=folium.Icon(color="orange", icon="home", prefix="fa"),
        ).add_to(m)

    try:
        folium.plugins.Geocoder(position="topleft", add_marker=False, collapsed=True).add_to(m)
    except Exception:
        pass

    folium.LayerControl(position="topright", collapsed=False).add_to(m)

    st_folium(m, use_container_width=True, height=height, returned_objects=[])


def single_property_map(prop: dict, height: int = 300) -> None:
    """
    Show a single property's exact location on a satellite map.
    """
    lat = prop.get("latitude")
    lon = prop.get("longitude")
    if not lat or not lon:
        lat, lon = AREA_COORDS.get(prop.get("locality", ""), (NELLORE_LAT, NELLORE_LON))

    m = folium.Map(
        location=[lat, lon],
        zoom_start=16,
        tiles=None,
        prefer_canvas=True,
    )

    folium.TileLayer(
        tiles=SATELLITE_TILES,
        attr=SATELLITE_ATTR,
        name="🛰️ Satellite",
        overlay=False,
        control=True,
    ).add_to(m)

    folium.TileLayer(
        tiles=HYBRID_LABELS_TILES,
        attr="Esri",
        name="🛰️ Satellite + Labels",
        overlay=True,
        control=True,
    ).add_to(m)

    folium.TileLayer("OpenStreetMap", name="🗺️ Street Map", overlay=False, control=True).add_to(m)

    icon_text = property_icon(prop["property_type"])
    price_str = format_price(prop["price"])
    popup_html = f"""
    <div style="font-family:sans-serif;min-width:160px;">
        <b>{prop['title']}</b><br>
        📍 {prop.get('locality', '')}<br>
        💰 <b>{price_str}</b>
    </div>
    """

    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=220),
        tooltip=f"📍 {prop.get('title', '')} — {price_str}",
        icon=folium.Icon(color="red", icon="home", prefix="fa"),
    ).add_to(m)

    folium.CircleMarker(
        location=[lat, lon],
        radius=10,
        color="#FF6B00",
        fill=True,
        fill_color="#FF6B00",
        fill_opacity=0.3,
    ).add_to(m)

    folium.LayerControl(position="topright", collapsed=True).add_to(m)

    st_folium(m, use_container_width=True, height=height, key=f"single_map_{prop.get('id', 'temp')}", returned_objects=[])
