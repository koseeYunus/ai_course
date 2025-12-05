"""
AI Vision Platform - Ana Uygulama
Modüler ve temiz kod yapısı
"""
import streamlit as st
import os
from config import TRANSLATIONS, FEEDBACK_DIR
from pages_ui import render_home, render_prediction_page

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="AI Vision Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MODERN STİLLENDİRME ---
st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    .stButton>button {
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# Feedback klasörünü oluştur
if not os.path.exists(FEEDBACK_DIR):
    os.makedirs(FEEDBACK_DIR)

# --- DURUM YÖNETİMİ ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = None
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None
if 'selected_model_type' not in st.session_state:
    st.session_state.selected_model_type = None
if 'feedback_given' not in st.session_state:
    st.session_state.feedback_given = False
if 'incorrect_clicked' not in st.session_state:
    st.session_state.incorrect_clicked = False
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# --- ANA PROGRAM ---
if __name__ == "__main__":
    if st.session_state.page == 'home':
        render_home(TRANSLATIONS, st.session_state.language)
    else:
        render_prediction_page(TRANSLATIONS, st.session_state.language, FEEDBACK_DIR)
