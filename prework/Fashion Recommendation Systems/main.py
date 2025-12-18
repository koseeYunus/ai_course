import streamlit as st
import os
import pickle
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import GlobalMaxPooling2D
from sklearn.neighbors import NearestNeighbors
from numpy.linalg import norm

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Moda AI", page_icon="🛍️", layout="wide")

# --- ÖZEL STİL ---
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-color: #ff4b4b; }
    .main { background-color: #ffffff; }
    div[data-testid="stExpander"] { border: none; box-shadow: none; }
    </style>
    """, unsafe_allow_html=True)

# --- MODEL VE VERİ YÜKLEME ---
@st.cache_resource
def load_model():
    base = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
    base.trainable = False
    return tf.keras.Sequential([base, GlobalMaxPooling2D()])

@st.cache_data
def load_data():
    features = pickle.load(open('src/Images_features.pkl', 'rb'))
    filenames = pickle.load(open('src/filenames.pkl', 'rb'))
    return np.array(features), filenames

# Verileri ve Modeli Hazırla
features, filenames = load_data()
model = load_model()

# Algoritma
nn = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
nn.fit(features)

# --- ARAYÜZ ---
st.title("🛍️ Moda AI: Akıllı Stil Arama")
st.markdown("Bir fotoğraf yükleyin, koleksiyonumuzdaki en benzer parçaları anında bulun.")
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

# Yan yana iki panel: Sol (Yükleme), Sağ (Sonuçlar)
col_left, col_right = st.columns([1, 3], gap="large")

with col_left:    
    if uploaded_file:
        user_img = Image.open(uploaded_file)
        st.image(user_img, caption="Aranan Stil", use_container_width=True)

with col_right:
    if uploaded_file:
        with st.spinner('Stilin analiz ediliyor ve eşleştiriliyor...'):
            # 1. Özellik Çıkarımı
            img_resized = user_img.convert("RGB").resize((224, 224))
            img_array = keras_image.img_to_array(img_resized)
            expanded_img = np.expand_dims(img_array, axis=0)
            preprocessed_img = preprocess_input(expanded_img)
            query_features = model.predict(preprocessed_img, verbose=0).flatten()
            query_features = query_features / norm(query_features)
            
            # 2. Arama
            distances, indices = nn.kneighbors([query_features])
            
            # 3. Sonuçları Göster
            st.subheader("🎯 Bulduğumuz Benzer Modeller")
            res_cols = st.columns(5)
            
            for i in range(5):
                idx = indices[0][i]
                dist = distances[0][i]
                sim_pct = max(0, 100 - (dist * 50))
                
                with res_cols[i]:
                    res_path = filenames[idx]
                    if os.path.exists(res_path):
                        st.image(Image.open(res_path), use_container_width=True)
                        st.write(f"**Benzerlik: %{sim_pct:.1f}**")
                        st.progress(sim_pct / 100)
