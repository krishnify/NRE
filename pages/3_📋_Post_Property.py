"""
NRE — Post Property Page
Sellers / agents can list their properties here.
Fixes:
  - property_type is selected OUTSIDE the form so BHK conditional re-renders dynamically
  - Photo upload with file save
  - Map location using st.map()
"""

import sys, os, uuid
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Post Property — NRE",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

from database.db import init_db, get_all_areas, add_property, update_property_images
from database.seed import seed
from utils.helpers import (
    PROPERTY_TYPES, FACING_LABELS, RESIDENTIAL_TYPES,
    format_price, AREA_COORDS, NELLORE_LAT, NELLORE_LON,
)



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

UPLOAD_DIR = Path(__file__).parent.parent / "assets" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("# 📋 Post Your Property")
st.markdown(
    "List your property for **free** and connect with thousands of buyers in Nellore. "
    "Fill in the details below — your contact info will be shown to interested buyers."
)
st.markdown("---")

all_areas = get_all_areas()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Property Type (OUTSIDE form so BHK section updates dynamically)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 🏠 Property Details")

top_col1, top_col2 = st.columns(2)
with top_col1:
    property_type = st.selectbox(
        "Property Type *",
        PROPERTY_TYPES,
        key="ptype_sel",
        help="Select the type — BHK/bathroom fields only appear for residential properties",
    )
with top_col2:
    locality = st.selectbox(
        "Locality / Area *",
        ["— Select Area —"] + all_areas,
        key="locality_sel",
    )

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — Core Details
# ─────────────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    title = st.text_input(
        "Property Title *",
        placeholder="e.g. 3 BHK Apartment in Trunk Road",
        help="Write a short, descriptive title",
    )
    price = st.number_input(
        "Price (₹) *",
        min_value=100_000,
        max_value=500_000_000,
        value=3_000_000,
        step=50_000,
        help="Enter price in Rupees. E.g. 5000000 = ₹50 Lakhs",
        format="%d",
    )
    facing = st.selectbox("Facing", ["—"] + FACING_LABELS)

with col2:
    size_sqft = st.number_input(
        "Size (sq.ft) *",
        min_value=100,
        max_value=1_000_000,
        value=1000,
        step=50,
    )
    age_years = st.number_input(
        "Property Age (years)",
        min_value=0,
        max_value=100,
        value=0,
        help="Enter 0 for brand new / under construction",
    )
    # Price preview
    st.markdown("")
    st.info(f"💰 **{format_price(int(price))}**", icon=None)

# ── BHK / Bathrooms — only shown for residential types ────────────────────────
show_bhk = property_type in RESIDENTIAL_TYPES
bedrooms = None
bathrooms = None

if show_bhk:
    st.markdown("#### 🛏 Rooms")
    bh_col1, bh_col2 = st.columns(2)
    with bh_col1:
        bedrooms = st.selectbox(
            "Bedrooms (BHK) *",
            [1, 2, 3, 4, 5, 6],
            index=1,
        )
    with bh_col2:
        bathrooms = st.selectbox(
            "Bathrooms *",
            [1, 2, 3, 4, 5],
            index=1,
        )

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — Description
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📝 Description")
description = st.text_area(
    "Property Description *",
    placeholder=(
        "Describe your property in detail — floor number, amenities, nearby landmarks, "
        "road width, water supply, power backup, furnishing status, etc. "
        "A good description attracts more buyers!"
    ),
    height=160,
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — Photo Upload
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📸 Property Photos")
st.caption("Upload up to 5 photos (JPG, PNG). First photo will be shown as the main image.")

uploaded_files = st.file_uploader(
    "Upload Photos",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True,
    label_visibility="collapsed",
)

if uploaded_files:
    # Limit to 5
    uploaded_files = uploaded_files[:5]
    preview_cols = st.columns(min(len(uploaded_files), 5))
    for i, uf in enumerate(uploaded_files):
        with preview_cols[i]:
            st.image(uf, use_container_width=True, caption=f"Photo {i+1}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — Location on Map  (Satellite + Google Maps style Search + Click-to-Pin)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📍 Property Location on Map")
st.caption(
    "Search any landmark, area, hospital, college, or street in Nellore (or click directly on the map) "
    "to pin your property location."
)

from components.map_component import make_folium_map
from utils.helpers import search_nellore_locations, NELLORE_LANDMARKS

# ── Resolve default coords from selected area ──────────────────────────────────
selected_loc = st.session_state.get("locality_sel", "— Select Area —")
area_lat, area_lon = AREA_COORDS.get(selected_loc, (NELLORE_LAT, NELLORE_LON))

# Reset to area coords ONLY when the locality dropdown actually changes
if st.session_state.get("_last_locality") != selected_loc:
    st.session_state["pin_lat"] = area_lat
    st.session_state["pin_lon"] = area_lon
    st.session_state["pin_label"] = f"Area: {selected_loc}" if selected_loc != "— Select Area —" else "Nellore City"
    st.session_state["_last_locality"] = selected_loc

if "pin_lat" not in st.session_state:
    st.session_state["pin_lat"] = area_lat
    st.session_state["pin_lon"] = area_lon
    st.session_state["pin_label"] = "Property Location"

# ── Landmark Callback (executes ONLY when user actively changes dropdown) ────
def on_landmark_chosen():
    chosen = st.session_state.get("quick_landmark_sel")
    if chosen and chosen != "— Or select a famous Nellore landmark —":
        for lm in NELLORE_LANDMARKS:
            if lm["name"] in chosen:
                st.session_state["pin_lat"] = lm["lat"]
                st.session_state["pin_lon"] = lm["lon"]
                st.session_state["pin_label"] = lm["name"]
                break

# ── 🔍 Search Box (Google Maps style) ─────────────────────────────────────────
with st.container(border=True):
    st.markdown("#### 🔍 Search Location / Landmark in Nellore")
    
    s_col1, s_col2 = st.columns([3, 1])
    with s_col1:
        map_search_input = st.text_input(
            "Search location",
            placeholder="Type any landmark or area: e.g. MGB Mall, Narayana Hospital, VRC Centre, Brodipet, Collectorate...",
            label_visibility="collapsed",
            key="map_search_query_input",
        )
    with s_col2:
        search_clicked = st.button("🔍 Find on Map", use_container_width=True, type="secondary")

    # Quick Landmark Picker dropdown (uses callback to avoid overwriting map clicks)
    landmark_options = ["— Or select a famous Nellore landmark —"] + [f"{lm['category']} {lm['name']} ({lm['area']})" for lm in NELLORE_LANDMARKS]
    st.selectbox(
        "Famous landmarks",
        landmark_options,
        index=0,
        label_visibility="collapsed",
        key="quick_landmark_sel",
        on_change=on_landmark_chosen,
    )

    # Handle text search
    if map_search_input.strip():
        search_results = search_nellore_locations(map_search_input.strip())
        if search_results:
            st.markdown(f"**Found {len(search_results)} matching locations:**")
            res_cols = st.columns(min(len(search_results), 3))
            for r_idx, res in enumerate(search_results):
                with res_cols[r_idx % min(len(search_results), 3)]:
                    if st.button(res["display"], key=f"search_loc_btn_{r_idx}", use_container_width=True):
                        st.session_state["pin_lat"] = res["lat"]
                        st.session_state["pin_lon"] = res["lon"]
                        st.session_state["pin_label"] = res["name"]
                        st.rerun()
        elif search_clicked:
            st.warning(f"No exact match found for '{map_search_input}'. You can click directly on the map or select an area above.")

# ── Render Satellite Map ───────────────────────────────────────────────────────
pin_lat = float(st.session_state["pin_lat"])
pin_lon = float(st.session_state["pin_lon"])
pin_label = st.session_state.get("pin_label", "Property Location")

st.info(f"📍 Current Pin: **{pin_label}** `(Latitude: {pin_lat:.6f}, Longitude: {pin_lon:.6f})` — Click anywhere on the map to place or adjust your pin.")

map_data = make_folium_map(
    lat=pin_lat,
    lon=pin_lon,
    zoom=16,
    height=450,
    marker_popup=pin_label,
    show_click_hint=True,
    key="folium_post_property_map",
)

# ── Handle map click → update pin coordinates permanently ─────────────────────
if map_data and map_data.get("last_clicked"):
    clicked_lat = round(float(map_data["last_clicked"]["lat"]), 6)
    clicked_lon = round(float(map_data["last_clicked"]["lng"]), 6)
    if (abs(clicked_lat - pin_lat) > 0.000005 or abs(clicked_lon - pin_lon) > 0.000005):
        st.session_state["pin_lat"] = clicked_lat
        st.session_state["pin_lon"] = clicked_lon
        st.session_state["pin_label"] = "Pinned on Map (Custom Location)"
        st.rerun()

# ── Confirmed Coordinates Display ─────────────────────────────────────────────
coord_col1, coord_col2 = st.columns(2)
with coord_col1:
    st.text_input(
        "📍 Latitude (Auto-captured from map click)",
        value=f"{st.session_state['pin_lat']:.6f}",
        disabled=True,
        help="Updates instantly when you click on the map above.",
    )
with coord_col2:
    st.text_input(
        "📍 Longitude (Auto-captured from map click)",
        value=f"{st.session_state['pin_lon']:.6f}",
        disabled=True,
        help="Updates instantly when you click on the map above.",
    )




# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 — Contact Details
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 👤 Your Contact Details")
st.caption("These will be shown to interested buyers.")

c1, c2, c3 = st.columns(3)
with c1:
    seller_name = st.text_input("Your Name *", placeholder="Full name or company name")
with c2:
    seller_phone = st.text_input(
        "Phone Number *",
        placeholder="10-digit mobile number",
        max_chars=10,
        help="Enter 10-digit mobile number without country code",
    )
with c3:
    seller_whatsapp = st.text_input(
        "WhatsApp Number",
        placeholder="Same as phone or different",
        max_chars=10,
        help="Leave blank if same as phone number",
    )

# ─────────────────────────────────────────────────────────────────────────────
# SUBMIT BUTTON
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("")
submitted = st.button("🚀 Post Property for FREE", use_container_width=True, type="primary")

# ─────────────────────────────────────────────────────────────────────────────
# VALIDATION & SAVE
# ─────────────────────────────────────────────────────────────────────────────
if submitted:
    errors = []

    if not title.strip():
        errors.append("Property title is required.")
    if locality == "— Select Area —":
        errors.append("Please select a locality.")
    if not description.strip() or len(description.strip()) < 30:
        errors.append("Description must be at least 30 characters.")
    if not seller_name.strip():
        errors.append("Your name is required.")
    if not seller_phone.strip() or not seller_phone.strip().isdigit() or len(seller_phone.strip()) != 10:
        errors.append("Please enter a valid 10-digit phone number.")

    if errors:
        for err in errors:
            st.error(f"❌ {err}")
    else:
        wa = seller_whatsapp.strip() if seller_whatsapp.strip() else seller_phone.strip()
        face = facing if facing != "—" else None

        prop_data = {
            "title":           title.strip(),
            "property_type":   property_type,
            "locality":        locality,
            "price":           int(price),
            "bedrooms":        bedrooms,
            "bathrooms":       bathrooms,
            "size_sqft":       int(size_sqft),
            "description":     description.strip(),
            "seller_name":     seller_name.strip(),
            "seller_phone":    seller_phone.strip(),
            "seller_whatsapp": wa,
            "facing":          face,
            "age_years":       int(age_years),
            "is_featured":     0,
            "status":          "Active",
            "images":          "",
            "latitude":        float(st.session_state["pin_lat"]),
            "longitude":       float(st.session_state["pin_lon"]),
        }

        new_id = add_property(prop_data)


        # ── Save uploaded images ───────────────────────────────────────────────
        saved_filenames = []
        if uploaded_files:
            prop_upload_dir = UPLOAD_DIR
            prop_upload_dir.mkdir(parents=True, exist_ok=True)
            for uf in uploaded_files:
                ext = Path(uf.name).suffix.lower() or ".jpg"
                fname = f"{new_id}_{uuid.uuid4().hex[:8]}{ext}"
                fpath = prop_upload_dir / fname
                with open(fpath, "wb") as f:
                    f.write(uf.getbuffer())
                saved_filenames.append(fname)

            if saved_filenames:
                update_property_images(new_id, ",".join(saved_filenames))

        st.balloons()
        st.success(
            f"✅ **Property listed successfully!** (ID: #{new_id})\n\n"
            f"Your property **\"{title.strip()}\"** is now live on NRE. "
            f"Buyers can see your listing and contact you at **{seller_phone.strip()}**.\n\n"
            f"🏷️ Listed Price: **{format_price(int(price))}**"
            + (f"  ·  📸 {len(saved_filenames)} photo(s) uploaded" if saved_filenames else "")
        )

        st.info(
            "💡 **Tips to get more enquiries:**\n"
            "- Share the website link on WhatsApp groups\n"
            "- Add more details in the description\n"
            "- Make sure your phone is reachable during the day"
        )

        if st.button("🔍 Browse All Listings"):
            st.switch_page("pages/2_🔍_Browse.py")

# ─────────────────────────────────────────────────────────────────────────────
# WHY LIST WITH US
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### Why list on NRE?")

wl_col1, wl_col2, wl_col3 = st.columns(3)
with wl_col1:
    with st.container(border=True):
        st.markdown("### 🆓")
        st.markdown("**100% Free**")
        st.caption("No commission, no hidden charges")
with wl_col2:
    with st.container(border=True):
        st.markdown("### ⚡")
        st.markdown("**Instant Listing**")
        st.caption("Goes live immediately after posting")
with wl_col3:
    with st.container(border=True):
        st.markdown("### 🎯")
        st.markdown("**Local Buyers**")
        st.caption("Reach buyers specifically in Nellore")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("🏠 **NRE — Nellore Real Estate**  ·  Nellore, Andhra Pradesh")
