"""
NRE — Browse & Search Page
Full property listing with sidebar filters + paginated grid.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from pathlib import Path
from database.db import init_db, search_properties, get_all_areas
from database.seed import seed
from components.property_card import render_property_card, _render_contact
from components.filters import render_filters
from utils.helpers import format_price

# ── Bootstrap ─────────────────────────────────────────────────────────────────
@st.cache_resource
def bootstrap():
    init_db()
    seed()
    return True

bootstrap()

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS_PATH = Path(__file__).parent.parent / "assets" / "style.css"
if CSS_PATH.exists():
    with open(CSS_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("# 🔍 Browse Properties")
st.markdown("Explore all available properties across Nellore city.")
st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────────────────────
filters = render_filters()

# ─────────────────────────────────────────────────────────────────────────────
# FETCH RESULTS
# ─────────────────────────────────────────────────────────────────────────────
PAGE_SIZE = 9

# Pagination state
if "browse_page" not in st.session_state:
    st.session_state["browse_page"] = 0

# Reset page when filters change (detect via key fingerprint)
filter_key = str(filters)
if st.session_state.get("_last_filter_key") != filter_key:
    st.session_state["browse_page"] = 0
    st.session_state["_last_filter_key"] = filter_key

offset = st.session_state["browse_page"] * PAGE_SIZE

all_results = search_properties(
    locality=filters["locality"],
    property_type=filters["property_type"],
    min_price=filters["min_price"],
    max_price=filters["max_price"],
    min_beds=filters["min_beds"],
    limit=500,  # Fetch all for sorting, then paginate in Python
)

# Sort
sort = filters.get("sort", "Newest First")
if sort == "Price: Low to High":
    all_results.sort(key=lambda x: x["price"])
elif sort == "Price: High to Low":
    all_results.sort(key=lambda x: x["price"], reverse=True)
elif sort == "Featured First":
    all_results.sort(key=lambda x: x.get("is_featured", 0), reverse=True)

total_results = len(all_results)
paginated = all_results[offset: offset + PAGE_SIZE]

# ─────────────────────────────────────────────────────────────────────────────
# ACTIVE FILTERS DISPLAY
# ─────────────────────────────────────────────────────────────────────────────
active_tags = []
if filters["locality"]:
    active_tags.append(f"📍 **Area:** {', '.join(filters['locality'])}")
if filters["property_type"]:
    active_tags.append(f"🏠 **Type:** {', '.join(filters['property_type'])}")
if filters["min_beds"]:
    active_tags.append(f"🛏 **BHK:** {filters['min_beds']}+")
if filters["min_price"] or filters["max_price"]:
    p_min = f"₹{filters['min_price']//100000}L" if filters["min_price"] else "₹0"
    p_max = f"₹{filters['max_price']//100000}L" if filters["max_price"] else "Any"
    active_tags.append(f"💰 **Budget:** {p_min} – {p_max}")

if active_tags:
    af_col1, af_col2 = st.columns([4, 1])
    with af_col1:
        st.info("  |  ".join(active_tags))
    with af_col2:
        if st.button("❌ Clear Filters", use_container_width=True):
            st.session_state["sidebar_locality"] = []
            st.session_state["sidebar_type"] = []
            st.session_state["sidebar_bhk"] = "Any"
            st.session_state["min_price_l"] = 0
            st.session_state["max_price_l"] = 0
            st.session_state["browse_page"] = 0
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# RESULTS HEADER
# ─────────────────────────────────────────────────────────────────────────────
rh_col1, rh_col2 = st.columns([3, 1])
with rh_col1:
    if total_results == 0:
        st.warning("No properties found matching your filters.")
        if st.button("View All Nellore Properties"):
            st.session_state["sidebar_locality"] = []
            st.session_state["sidebar_type"] = []
            st.session_state["sidebar_bhk"] = "Any"
            st.session_state["min_price_l"] = 0
            st.session_state["max_price_l"] = 0
            st.session_state["browse_page"] = 0
            st.rerun()
    else:
        start = offset + 1
        end = min(offset + PAGE_SIZE, total_results)
        st.markdown(f"**{total_results} properties found** — showing {start}–{end}")

with rh_col2:
    if total_results > 0:
        st.markdown(f"*Page {st.session_state['browse_page'] + 1} of {max(1, -(-total_results // PAGE_SIZE))}*")

st.markdown("")

# ─────────────────────────────────────────────────────────────────────────────
# PROPERTY GRID
# ─────────────────────────────────────────────────────────────────────────────
if paginated:
    cols = st.columns(3)
    for i, prop in enumerate(paginated):
        with cols[i % 3]:
            render_property_card(prop, show_contact=False, card_key=f"browse_{prop['id']}")

            with st.expander("📋 Full Details, Photos & Contact"):
                from components.property_card import render_property_full_details
                render_property_full_details(prop)


# ─────────────────────────────────────────────────────────────────────────────
# PAGINATION CONTROLS
# ─────────────────────────────────────────────────────────────────────────────
if total_results > PAGE_SIZE:
    st.markdown("---")
    total_pages = -(-total_results // PAGE_SIZE)  # ceiling division
    current_page = st.session_state["browse_page"]

    pg_col1, pg_col2, pg_col3 = st.columns([1, 2, 1])

    with pg_col1:
        if current_page > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state["browse_page"] -= 1
                st.rerun()

    with pg_col2:
        st.markdown(
            f"<div style='text-align:center;padding-top:0.5rem;color:#6B7280;'>"
            f"Page <strong>{current_page + 1}</strong> of <strong>{total_pages}</strong>"
            f"</div>",
            unsafe_allow_html=True,
        )

    with pg_col3:
        if current_page < total_pages - 1:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state["browse_page"] += 1
                st.rerun()

# Also show map of all filtered listings if they have coordinates
has_coords = [p for p in all_results if p.get("latitude") and p.get("longitude")]
if has_coords:
    with st.expander(f"🛰️ Show {len(has_coords)} properties on Satellite Map"):
        from components.map_component import properties_overview_map
        properties_overview_map(has_coords, height=420)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("🏠 **NRE — Nellore Real Estate**  ·  Nellore, Andhra Pradesh")
