"""Sidebar filter widget for Browse page."""

import streamlit as st
from database.db import get_all_areas
from utils.helpers import PROPERTY_TYPES


def render_filters() -> dict:
    """Render sidebar filters and return the selected filter values."""
    st.sidebar.markdown("## 🔍 Filter Properties")
    st.sidebar.markdown("---")

    all_areas = get_all_areas()

    # Ensure key state exists if needed
    if "sidebar_locality" not in st.session_state:
        st.session_state["sidebar_locality"] = []

    # Filter out any non-existent areas just in case
    current_selected = [a for a in st.session_state["sidebar_locality"] if a in all_areas]
    st.session_state["sidebar_locality"] = current_selected

    # Area multi-select
    selected_areas = st.sidebar.multiselect(
        "📍 Locality / Area",
        options=all_areas,
        key="sidebar_locality",
        placeholder="All areas",
        help="Select one or more localities",
    )

    # Property type
    if "sidebar_type" not in st.session_state:
        st.session_state["sidebar_type"] = []

    selected_types = st.sidebar.multiselect(
        "🏠 Property Type",
        options=PROPERTY_TYPES,
        key="sidebar_type",
        placeholder="All types",
    )

    # BHK filter
    if "sidebar_bhk" not in st.session_state:
        st.session_state["sidebar_bhk"] = "Any"

    bhk_options = ["Any", "1+", "2+", "3+", "4+"]
    bhk_index = bhk_options.index(st.session_state["sidebar_bhk"]) if st.session_state["sidebar_bhk"] in bhk_options else 0
    bhk_sel = st.sidebar.selectbox("🛏 Minimum BHK", bhk_options, index=bhk_index, key="sidebar_bhk")
    min_beds = 0
    if bhk_sel != "Any":
        min_beds = int(bhk_sel.replace("+", ""))

    st.sidebar.markdown("---")

    # Price range
    st.sidebar.markdown("**💰 Price Range**")
    price_col1, price_col2 = st.sidebar.columns(2)
    with price_col1:
        min_price_l = st.number_input(
            "Min (Lakhs)", min_value=0, max_value=10000, step=5,
            key="min_price_l"
        )
    with price_col2:
        max_price_l = st.number_input(
            "Max (Lakhs)", min_value=0, max_value=10000, step=5,
            key="max_price_l"
        )

    min_price = int(min_price_l * 100_000) if min_price_l > 0 else None
    max_price = int(max_price_l * 100_000) if max_price_l > 0 else None

    st.sidebar.markdown("---")

    # Sort
    if "sidebar_sort" not in st.session_state:
        st.session_state["sidebar_sort"] = "Newest First"

    sort_options = ["Newest First", "Price: Low to High", "Price: High to Low", "Featured First"]
    sort_index = sort_options.index(st.session_state["sidebar_sort"]) if st.session_state["sidebar_sort"] in sort_options else 0
    sort_opt = st.sidebar.selectbox(
        "⬆️ Sort By",
        sort_options,
        index=sort_index,
        key="sidebar_sort",
    )

    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
        st.session_state["sidebar_locality"] = []
        st.session_state["sidebar_type"] = []
        st.session_state["sidebar_bhk"] = "Any"
        st.session_state["min_price_l"] = 0
        st.session_state["max_price_l"] = 0
        st.session_state["sidebar_sort"] = "Newest First"
        st.session_state["browse_page"] = 0
        st.rerun()

    st.sidebar.caption("🏙️ **Nellore Real Estate**\nYour trusted property platform")

    return {
        "locality": selected_areas if selected_areas else None,
        "property_type": selected_types if selected_types else None,
        "min_price": min_price,
        "max_price": max_price,
        "min_beds": min_beds,
        "sort": sort_opt,
    }
