"""Reusable luxury property card and detailed view components for NRE."""

import streamlit as st
from pathlib import Path
from utils.helpers import (
    format_price, format_area, bhk_label, property_icon,
    whatsapp_link, days_ago
)

UPLOAD_DIR = Path(__file__).parent.parent / "assets" / "uploads"


def get_valid_images(prop: dict) -> list[Path]:
    """Return a list of existing image Paths for a property."""
    images_str = prop.get("images", "")
    if not images_str:
        return []
    image_files = [f.strip() for f in images_str.split(",") if f.strip()]
    valid = []
    for img_file in image_files:
        img_path = UPLOAD_DIR / img_file
        if img_path.exists():
            valid.append(img_path)
    return valid


# ── Full Property Details Dialog (Modal) ───────────────────────────────────────
if hasattr(st, "dialog"):
    @st.dialog("🏠 Property Details", width="large")
    def open_property_modal(prop: dict):
        render_property_full_details(prop, in_dialog=True)
else:
    def open_property_modal(prop: dict):
        render_property_full_details(prop, in_dialog=False)


def render_property_full_details(prop: dict, in_dialog: bool = False):
    """
    Render all details of a property, including ALL uploaded photos,
    pricing, specs, full description, satellite map, and direct WhatsApp/Phone contacts.
    """
    icon = property_icon(prop["property_type"])
    price_str = format_price(prop["price"])
    posted = days_ago(prop.get("posted_date", ""))
    sqft = prop.get("size_sqft")
    price_per_sqft = f"₹{prop['price'] // sqft:,}/sq.ft" if sqft and sqft > 0 else None

    # Title & Location Header
    st.markdown(f"## {prop['title']}")
    st.markdown(
        f"<span style='color:#0F766E;font-weight:700;font-size:1.05rem;'>📍 {prop.get('locality', '')}</span>  ·  "
        f"<span style='color:#64748B;'>{icon} {prop['property_type']}</span>  ·  "
        f"<span style='color:#94A3B8;'>Listed {posted}</span>",
        unsafe_allow_html=True,
    )

    # ── Luxury Price Banner ────────────────────────────────────────────────────
    with st.container(border=True):
        p_col1, p_col2 = st.columns([2, 1])
        with p_col1:
            st.markdown(
                f"<div style='font-family:Outfit,sans-serif;font-size:2rem;font-weight:800;color:#E85D04;line-height:1.2;'>"
                f"{price_str}</div>",
                unsafe_allow_html=True,
            )
            if price_per_sqft:
                st.caption(f"Estimated Rate: **{price_per_sqft}**")
        with p_col2:
            status = prop.get("status", "Active")
            status_color = "#0F766E" if status == "Active" else "#E85D04"
            st.markdown(
                f"<div style='text-align:right;'><span style='background:{status_color}18;color:{status_color};"
                f"font-weight:700;padding:6px 14px;border-radius:20px;font-size:0.85rem;border:1px solid {status_color}33;'>"
                f"● {status}</span></div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ALL PHOTOS GALLERY ─────────────────────────────────────────────────────
    images = get_valid_images(prop)
    st.markdown(f"### 📸 Photo Gallery ({len(images)})")

    if images:
        if len(images) == 1:
            st.image(str(images[0]), use_container_width=True, caption=f"{prop['title']} — High Resolution Photo")
        else:
            tabs = st.tabs([f"🖼️ Photo {i+1}" for i in range(len(images))])
            for i, img_path in enumerate(images):
                with tabs[i]:
                    st.image(str(img_path), use_container_width=True, caption=f"Photo {i+1} of {len(images)}")
            
            with st.expander(f"🔍 View all {len(images)} photos in grid"):
                photo_cols = st.columns(min(len(images), 3))
                for i, img_path in enumerate(images):
                    with photo_cols[i % 3]:
                        st.image(str(img_path), use_container_width=True, caption=f"Photo {i+1}")
    else:
        st.markdown(
            f"<div style='background:linear-gradient(135deg,#FFF7ED,#F0FDFA);"
            f"border-radius:14px;height:180px;display:flex;align-items:center;"
            f"justify-content:center;font-size:4rem;border:1px dashed #E2E8F0;'>"
            f"{icon}</div>",
            unsafe_allow_html=True,
        )
        st.caption("No photos uploaded for this property.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PROPERTY SPECIFICATIONS ────────────────────────────────────────────────
    st.markdown("### 📋 Property Overview & Specifications")
    specs = []
    if prop.get("bedrooms"):
        specs.append(("🛏 Bedrooms", f"{prop['bedrooms']} BHK"))
    if prop.get("bathrooms"):
        specs.append(("🚿 Bathrooms", f"{prop['bathrooms']}"))
    if prop.get("size_sqft"):
        specs.append(("📐 Built-up Area", f"{prop['size_sqft']:,} sq.ft"))
    if prop.get("facing"):
        specs.append(("🧭 Facing", prop["facing"]))
    if prop.get("age_years") is not None:
        specs.append(("🏗 Property Age", "Brand New" if prop["age_years"] == 0 else f"{prop['age_years']} Years"))
    specs.append(("🏠 Type", prop["property_type"]))
    specs.append(("📍 Locality", prop["locality"]))

    spec_cols = st.columns(3)
    for i, (label, val) in enumerate(specs):
        with spec_cols[i % 3]:
            with st.container(border=True):
                st.caption(label)
                st.markdown(f"**{val}**")

    # ── DESCRIPTION ───────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📝 Detailed Description")
    desc = prop.get("description", "").strip()
    if desc:
        with st.container(border=True):
            st.markdown(desc)
    else:
        st.caption("No additional description provided.")

    # ── SATELLITE MAP LOCATION ─────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📍 Satellite Map Location")
    try:
        from components.map_component import single_property_map
        single_property_map(prop, height=320)
    except Exception:
        st.caption(f"📍 Location: {prop.get('locality', 'Nellore')}")

    # ── SELLER / AGENT CONTACT ─────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📞 Verified Seller & Agent Contact")
    _render_contact(prop, f"detail_contact_{prop['id']}")


def render_property_card(prop: dict, show_contact: bool = False, card_key: str = ""):
    """Render a luxury property card with sleek badge, typography, and clear action button."""
    icon = property_icon(prop["property_type"])
    price_str = format_price(prop["price"])
    posted = days_ago(prop.get("posted_date", ""))

    beds = prop.get("bedrooms")
    baths = prop.get("bathrooms")
    sqft = prop.get("size_sqft")
    facing = prop.get("facing", "")
    age = prop.get("age_years", 0)
    is_featured = prop.get("is_featured", 0)

    images = get_valid_images(prop)
    num_images = len(images)

    with st.container(border=True):
        # Featured badge
        if is_featured:
            st.markdown(
                "<span style='background:linear-gradient(135deg,#E85D04,#FF7700);color:white;font-size:0.72rem;"
                "font-weight:700;padding:4px 12px;border-radius:20px;"
                "text-transform:uppercase;letter-spacing:0.06em;box-shadow:0 2px 8px rgba(232,93,4,0.3);'>⭐ Featured</span>",
                unsafe_allow_html=True,
            )

        # ── Primary Image with Photo Count ─────────────────────────────────────
        if images:
            st.image(str(images[0]), use_container_width=True)
            if num_images > 1:
                st.caption(f"📸 **1 of {num_images} Photos**")
        else:
            st.markdown(
                f"<div style='background:linear-gradient(135deg,#FFF7ED,#F0FDFA);"
                f"border-radius:12px;height:150px;display:flex;align-items:center;"
                f"justify-content:center;font-size:3.2rem;margin-bottom:0.5rem;"
                f"border:1px dashed #E2E8F0;'>{icon}</div>",
                unsafe_allow_html=True,
            )

        # Type badge
        st.caption(f"{icon} {prop['property_type']}")

        # Title
        st.markdown(f"**{prop['title']}**")

        # Locality
        locality = prop.get("locality", "")
        st.markdown(
            f"<span style='color:#0F766E;font-weight:600;font-size:0.90rem;'>"
            f"📍 {locality}</span>",
            unsafe_allow_html=True,
        )

        # Price
        st.markdown(
            f"<div style='font-family:Outfit,sans-serif;font-size:1.45rem;font-weight:800;color:#E85D04;"
            f"margin:0.35rem 0;'>{price_str}</div>",
            unsafe_allow_html=True,
        )

        # Meta chips
        meta_parts = []
        if beds:
            meta_parts.append(f"🛏 {bhk_label(beds)}")
        if baths:
            meta_parts.append(f"🚿 {baths} Bath")
        if sqft:
            meta_parts.append(f"📐 {format_area(sqft)}")
        if facing:
            meta_parts.append(f"🧭 {facing}")
        if age is not None:
            meta_parts.append(f"🏗 {'New' if age == 0 else f'{age}yr'}")

        if meta_parts:
            st.caption("  ·  ".join(meta_parts))

        # Description preview
        desc = prop.get("description", "")
        if desc:
            preview = desc[:140] + "…" if len(desc) > 140 else desc
            st.markdown(
                f"<div style='font-size:0.84rem;color:#64748B;line-height:1.45;"
                f"margin:0.3rem 0;'>{preview}</div>",
                unsafe_allow_html=True,
            )

        # Footer
        fc1, fc2 = st.columns(2)
        with fc1:
            st.caption(f"🕐 {posted}")
        with fc2:
            st.caption(f"👤 {prop.get('seller_name', '')}")

        # View Full Details Button
        btn_label = f"🔍 View All Details & Photos ({num_images})" if num_images > 0 else "🔍 View All Details"
        if st.button(btn_label, key=f"view_btn_{card_key}_{prop['id']}", use_container_width=True, type="primary"):
            open_property_modal(prop)

    if show_contact:
        _render_contact(prop, card_key)


def _render_contact(prop: dict, card_key: str):
    """Render contact details with phone and direct WhatsApp chat button."""
    seller = prop.get("seller_name", "N/A")
    phone = prop.get("seller_phone", "")
    wa_num = prop.get("seller_whatsapp", phone)
    wa_link = whatsapp_link(wa_num, prop.get("title", "this property"))

    with st.container(border=True):
        st.markdown(f"### 🤝 {seller}")
        st.markdown(
            f"<div style='font-size:1.2rem;font-weight:700;color:#0F766E;margin:4px 0;'>"
            f"📞 <a href='tel:{phone}' style='color:#0F766E;text-decoration:none;'>{phone}</a></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<a href="{wa_link}" target="_blank" style="background:linear-gradient(135deg,#25D366,#1EBE5D);color:white;'
            f'border-radius:24px;padding:8px 24px;font-weight:700;font-size:0.95rem;box-shadow:0 4px 14px rgba(37,211,102,0.35);'
            f'text-decoration:none;display:inline-block;margin-top:8px;">💬 Chat on WhatsApp</a>',
            unsafe_allow_html=True,
        )
        st.caption(f"📍 {prop.get('locality')}  ·  {prop['property_type']}  ·  {format_price(prop['price'])}")
