"""
NRE — Home Page
Hero banner, stats strip, featured listings, area explorer.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="NRE — Nellore Real Estate",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

from database.db import (
    init_db, search_properties, total_property_count,
    total_area_count, get_all_areas, get_areas_with_count,
)
from database.seed import seed
from components.property_card import render_property_card, _render_contact
from utils.helpers import format_price, PROPERTY_TYPES


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
# LUXURY HERO BANNER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nre-hero-luxury">
    <div class="nre-hero-badge">✨ PREMIER PROPERTY NETWORK · ANDHRA PRADESH</div>
    <h1>Discover Exceptional Real Estate in <span>Nellore</span></h1>
    <p>Explore verified luxury villas, modern apartments, commercial spaces, and residential plots across 71 prime localities with direct seller contacts.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ELEVATED QUICK SEARCH CAPSULE
# ─────────────────────────────────────────────────────────────────────────────
all_areas = get_all_areas()

with st.container(border=True):
    st.markdown("#### 🔍 Find Your Dream Property")
    qs_col1, qs_col2, qs_col3, qs_col4 = st.columns([3, 2, 2, 1.8])

    with qs_col1:
        st.caption("📍 Select Locality")
        qs_area = st.selectbox(
            "Locality", ["Any Area"] + all_areas,
            label_visibility="collapsed",
            key="qs_area",
        )
    with qs_col2:
        st.caption("🏠 Property Type")
        qs_type = st.selectbox(
            "Property Type", ["Any Type"] + PROPERTY_TYPES,
            label_visibility="collapsed",
            key="qs_type",
        )
    with qs_col3:
        st.caption("💰 Budget Range")
        qs_budget = st.selectbox(
            "Budget", ["Any Budget", "Under ₹20L", "₹20L–₹50L", "₹50L–₹1Cr", "₹1Cr+"],
            label_visibility="collapsed",
            key="qs_budget",
        )
    with qs_col4:
        st.caption("&nbsp;")
        search_clicked = st.button("🚀 Explore Properties", use_container_width=True, type="primary")

if search_clicked:
    st.session_state["sidebar_locality"] = [qs_area] if qs_area != "Any Area" else []
    st.session_state["sidebar_type"] = [qs_type] if qs_type != "Any Type" else []
    budget_map = {
        "Under ₹20L":  (0, 20),
        "₹20L–₹50L":  (20, 50),
        "₹50L–₹1Cr":  (50, 100),
        "₹1Cr+":      (100, 0),
    }
    bmin, bmax = budget_map.get(qs_budget, (0, 0))
    st.session_state["min_price_l"] = bmin
    st.session_state["max_price_l"] = bmax
    st.session_state["browse_page"] = 0
    st.switch_page("pages/2_🔍_Browse.py")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STATS STRIP
# ─────────────────────────────────────────────────────────────────────────────
total_props = total_property_count()
total_areas = total_area_count()
featured_count = len(search_properties(featured_only=True))

sc1, sc2, sc3, sc4 = st.columns(4)
sc1.metric("🏠 Active Listings", total_props)
sc2.metric("📍 Localities", total_areas)
sc3.metric("⭐ Verified & Featured", featured_count)
sc4.metric("⚡ Direct Connect", "100% Free")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FEATURED LISTINGS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("## ⭐ Handpicked Featured Properties")
st.caption("Prime listings curated for quality, location, and verified seller details.")

featured = search_properties(featured_only=True, limit=6)

if featured:
    cols = st.columns(3)
    for i, prop in enumerate(featured):
        with cols[i % 3]:
            render_property_card(prop, show_contact=False, card_key=f"feat_{prop['id']}")
            with st.expander("📋 Full Details, Photos & Contact"):
                from components.property_card import render_property_full_details
                render_property_full_details(prop)
else:
    st.info("No featured properties yet. Be the first to post!")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LATEST LISTINGS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("## 🆕 Latest Market Listings")
st.caption("Freshly added residential and commercial opportunities across Nellore.")

latest = search_properties(limit=12)
latest_non_feat = [p for p in latest if not p.get("is_featured")][:6]

if latest_non_feat:
    cols2 = st.columns(3)
    for i, prop in enumerate(latest_non_feat):
        with cols2[i % 3]:
            render_property_card(prop, show_contact=False, card_key=f"lat_{prop['id']}")
            with st.expander("📋 Full Details, Photos & Contact"):
                from components.property_card import render_property_full_details
                render_property_full_details(prop)

# ─────────────────────────────────────────────────────────────────────────────
# AREA EXPLORER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 🗺️ Explore by Locality")
st.caption("Select any locality below to view properties available in that neighborhood.")

areas_data = get_areas_with_count()
areas_with_props = [a for a in areas_data if a["property_count"] > 0][:20]

ZONE_ICON = {"Central": "🏛️", "North": "⬆️", "South": "⬇️", "East": "➡️", "West": "⬅️"}

if areas_with_props:
    area_cols = st.columns(4)
    for i, area in enumerate(areas_with_props):
        with area_cols[i % 4]:
            with st.container(border=True):
                zone_icon = ZONE_ICON.get(area["zone"], "📍")
                count = area["property_count"]
                st.markdown(f"#### {zone_icon}")
                st.markdown(f"**{area['name']}**")
                st.markdown(
                    f"<span style='color:#E85D04;font-size:0.85rem;font-weight:700;'>"
                    f"{count} {'listing' if count == 1 else 'listings'}</span>  "
                    f"<span style='color:#64748B;font-size:0.75rem;'>· {area['zone']}</span>",
                    unsafe_allow_html=True,
                )
                if st.button(f"View Properties →", key=f"area_btn_{i}_{area['name']}", use_container_width=True):
                    st.session_state["sidebar_locality"] = [area["name"]]
                    st.session_state["sidebar_type"] = []
                    st.session_state["min_price_l"] = 0
                    st.session_state["max_price_l"] = 0
                    st.session_state["sidebar_bhk"] = "Any"
                    st.session_state["browse_page"] = 0
                    st.switch_page("pages/2_🔍_Browse.py")

with st.expander(f"📋 Browse all {len(areas_data)} Nellore Localities & Zones"):
    all_cols = st.columns(4)
    for i, area in enumerate(areas_data):
        with all_cols[i % 4]:
            count = area["property_count"]
            badge = f"({count})" if count > 0 else ""
            if st.button(f"📍 {area['name']} {badge}", key=f"all_area_btn_{i}_{area['name']}", use_container_width=True):
                st.session_state["sidebar_locality"] = [area["name"]]
                st.session_state["sidebar_type"] = []
                st.session_state["min_price_l"] = 0
                st.session_state["max_price_l"] = 0
                st.session_state["sidebar_bhk"] = "Any"
                st.session_state["browse_page"] = 0
                st.switch_page("pages/2_🔍_Browse.py")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nre-footer-luxury">
    <div style="font-weight:700; color:#0A0F1D; font-size:1.05rem; margin-bottom:0.3rem;">
        🏠 NRE — Nellore Real Estate Network
    </div>
    <div style="color:#64748B; font-size:0.85rem;">
        Connecting Buyers, Sellers & Real Estate Agents across Nellore, Andhra Pradesh
    </div>
    <div style="margin-top:0.8rem; font-size:0.78rem; color:#94A3B8;">
        © 2026 Nellore Real Estate Platform. All rights reserved.
    </div>
</div>
""", unsafe_allow_html=True)
