"""
NRE — Nellore Real Estate
Main entry point — initialises DB, injects CSS, and redirects to Home.
"""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from pathlib import Path
from database.db import init_db
from database.seed import seed

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NRE — Nellore Real Estate",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS Injection ─────────────────────────────────────────────────────────────
CSS_PATH = Path(__file__).parent / "assets" / "style.css"
if CSS_PATH.exists():
    with open(CSS_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── DB Init & Seed (once per session) ─────────────────────────────────────────
@st.cache_resource
def bootstrap():
    init_db()
    seed()
    return True

bootstrap()

# ── Landing redirect ───────────────────────────────────────────────────────────
st.switch_page("pages/1_🏠_Home.py")
