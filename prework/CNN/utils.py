"""
Yardımcı fonksiyonlar
"""
import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
import os


@st.cache_resource
def load_model_file(model_path):
    """
    Modeli cache'e alarak yükler, böylece her tahmin işleminde tekrar yüklenmez.
    """
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Model yüklenirken hata oluştu: {e}")
        return None


def preprocess_image(image, target_size=(224, 224)):
    """
    Görseli modelin beklediği formata getirir.
    """
    image = ImageOps.fit(image, target_size, Image.LANCZOS)
    img_array = np.array(image)
    img_array = img_array.astype("float32") / 255.0  # 0-1 arası normalize et
    img_array = np.expand_dims(img_array, axis=0)  # Batch boyutu ekle
    return img_array


def save_feedback(image, topic, model_type, predicted_label, actual_label, is_correct, feedback_dir):
    """
    Kullanıcı geri bildirimini ve resmi kaydeder.
    Yanlış tahminlerde hem tahmin edilen hem de gerçek sınıf bilgisi kaydedilir.
    """
    # Alt klasör oluştur
    topic_folder = os.path.join(feedback_dir, topic.replace(" ", "_"))
    if not os.path.exists(topic_folder):
        os.makedirs(topic_folder)
    
    if is_correct:
        # Aynı isimde dosya varsa üzerine yazılmasın diye sayaç ekle
        base_filename = f"{model_type}_correct_{predicted_label}"
        counter = 1
        filename = f"{base_filename}.png"
        save_path = os.path.join(topic_folder, filename)
        while os.path.exists(save_path):
            filename = f"{base_filename}_{counter}.png"
            save_path = os.path.join(topic_folder, filename)
            counter += 1
    else:
        base_filename = f"{model_type}_incorrect_predicted-{predicted_label}_actual-{actual_label}"
        counter = 1
        filename = f"{base_filename}.png"
        save_path = os.path.join(topic_folder, filename)
        while os.path.exists(save_path):
            filename = f"{base_filename}_{counter}.png"
            save_path = os.path.join(topic_folder, filename)
            counter += 1
    
    # Resmi kaydet
    image.save(save_path)
    return save_path


def get_text(translations, language, key):
    """Dil seçimine göre metni döndürür"""
    return translations[language][key]
