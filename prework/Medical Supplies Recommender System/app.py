import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Sayfa Ayarları
st.set_page_config(page_title="Medikal Tavsiye Sistemi", layout="wide")

# --- 1. MODELİ YÜKLEME FONKSİYONU (Önbellek Kullanımı) ---
@st.cache_resource
def load_system():
    try:
        # Scriptin bulunduğu klasör yolunu dinamik olarak al
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'medical_recommender.pkl')
        
        # Dosyayı tam yol ile yükle
        data = joblib.load(file_path)
        return data
    except FileNotFoundError:
        st.error(f"HATA: Dosya bulunamadı! Aranan yol: {file_path}")
        return None

# Sistemi Yükle
system_data = load_system()

if system_data:
    # Değişkenleri ayrıştıralım
    svd = system_data['svd_model']
    user_item_matrix = system_data['user_item_matrix']
    matrix_decomposed = system_data['matrix_decomposed']
    cosine_sim = system_data['cosine_sim']
    product_id_to_name = system_data['product_id_to_name']
    id_to_index = system_data['id_to_index']
    products_content = system_data['products_content']
    popular_products = system_data['popular_products']

    # --- 2. ÖNERİ FONKSİYONLARI ---

    # A. İçerik Bazlı (Ürün Benzerliği)
    def recommend_similar_products(product_id, n=5):
        if product_id not in id_to_index:
            return None
        
        idx = id_to_index[product_id]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1] # Kendisi hariç ilk n tanesi
        
        product_indices = [i[0] for i in sim_scores]
        # Sonuçları DataFrame olarak döndür
        return products_content.iloc[product_indices][['product_name', 'description']]

    # B. İşbirlikçi Filtreleme (SVD - Kişiye Özel)
    def recommend_for_user(user_id, n=5, filter_bought=False):
        if user_id not in user_item_matrix.index:
            return "new_user" # Yeni kullanıcı bayrağı
        
        user_idx = user_item_matrix.index.get_loc(user_id)
        
        # Kullanıcı vektörü ile ürün özelliklerinin çarpımı (Tahmin Skoru)
        user_latent_vector = matrix_decomposed[user_idx].reshape(1, -1)
        predicted_scores = np.dot(user_latent_vector, svd.components_).flatten()
        
        # Filtreleme opsiyonu
        if filter_bought:
            user_original_ratings = user_item_matrix.iloc[user_idx].values
            predicted_scores[user_original_ratings > 0] = -np.inf
        
        # En yüksek skorlu n ürünü bul
        top_indices = predicted_scores.argsort()[::-1][:n]
        
        recs = []
        for idx in top_indices:
            prod_id = user_item_matrix.columns[idx]
            prod_name = product_id_to_name.get(prod_id, f"Ürün {prod_id}")
            recs.append(prod_name)
            
        return recs

    # --- 3. ARAYÜZ TASARIMI (UI) ---
    
    st.title("🏥 Akıllı Tıbbi Malzeme Tavsiye Sistemi")
    st.markdown("---")

    # Yan Menü (Sidebar)
    st.sidebar.header("Öneri Modu Seçiniz")
    mode = st.sidebar.radio(
        "Senaryo:",
        ("Kişiye Özel Öneri (User-Based)", "Ürün Benzerliği (Content-Based)", "Popüler Ürünler (Best Sellers)")
    )

    # --- SENARYO 1: KULLANICI BAZLI ---
    if mode == "Kişiye Özel Öneri (User-Based)":
        st.subheader("👤 Müşteri Satın Alma Geçmişine Göre Öneriler")
        st.info("SVD (Matrix Factorization) algoritması kullanılarak müşterinin gizli tercihleri analiz edilir.")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            # Kullanıcı ID Girişi (Örnek olarak listedeki ilk 10 ID'yi ipucu verelim)
            sample_ids = user_item_matrix.index[:10].tolist()
            user_id_input = st.number_input("Müşteri ID Giriniz:", min_value=1, value=sample_ids[0], step=1)
            
            filter_option = st.checkbox("Daha önce aldıklarını gizle?", value=False)
            num_recs = st.slider("Öneri Sayısı", 3, 10, 5)

        with col2:
            if st.button("Önerileri Getir"):
                results = recommend_for_user(user_id_input, n=num_recs, filter_bought=filter_option)
                
                if results == "new_user":
                    st.warning(f"⚠️ ID: {user_id_input} veritabanında bulunamadı. Bu yeni bir müşteri olabilir.")
                    st.success("✅ 'Cold Start' stratejisi devreye girdi. En popüler ürünler öneriliyor:")
                    st.table(pd.DataFrame(popular_products[:num_recs], columns=["Genel Popüler Ürünler"]))
                else:
                    st.success(f"✅ Müşteri {user_id_input} için SVD Tahminleri:")
                    # Sonuçları güzel bir liste olarak göster
                    for i, prod in enumerate(results, 1):
                        st.write(f"**{i}.** {prod}")

    # --- SENARYO 2: İÇERİK BAZLI ---
    elif mode == "Ürün Benzerliği (Content-Based)":
        st.subheader("📦 Ürün Benzerliğine Göre Öneriler")
        st.info("NLP (TF-IDF) kullanılarak ürün açıklamaları analiz edilir ve en benzer ürünler bulunur.")
        
        # Ürün Seçimi (Selectbox ile)
        # Hız için sadece ilk 100 ürünü listeye koyalım, ya da ID girişi yaptıralım
        # Burada örnek olarak ID girişi yapıyoruz
        sample_prod_id = products_content.index[0]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            prod_id_input = st.number_input("Ürün ID Giriniz:", min_value=1, value=int(sample_prod_id), step=1)
            
            # Seçilen ürünün adını gösterelim
            if prod_id_input in product_id_to_name:
                st.write(f"**Seçilen Ürün:** {product_id_to_name[prod_id_input]}")
            else:
                st.write("**Seçilen Ürün:** Bulunamadı")
                
        with col2:
            if st.button("Benzer Ürünleri Bul"):
                similar_products_df = recommend_similar_products(prod_id_input)
                
                if similar_products_df is None:
                    st.error("Bu ID'ye ait ürün bulunamadı.")
                else:
                    st.success("✅ Benzer Özellikteki Ürünler:")
                    st.table(similar_products_df['product_name'])
                    
                    with st.expander("Detaylı Açıklamaları Gör"):
                        st.table(similar_products_df)

    # --- SENARYO 3: POPÜLERLİK ---
    else:
        st.subheader("🔥 En Çok Satan Ürünler")
        st.info("Herhangi bir kullanıcı verisi olmadığında (Anasayfa Vitrini) gösterilecek ürünler.")
        
        st.table(pd.DataFrame(popular_products, columns=["En Popüler Ürünler"]))

    # Alt Bilgi
    st.markdown("---")
    st.caption("Developed with Streamlit & Scikit-Learn | Medical Recommender System v1.0")

else:
    st.stop()