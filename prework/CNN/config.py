"""
Uygulama konfigürasyonu ve çeviriler
"""

# --- ÇEVİRİLER ---
TRANSLATIONS = {
    "tr": {
        "title": "🎯 Yapay Zeka Görüntü Platformu",
        "subtitle": "Derin Öğrenme & Transfer Öğrenme",
        "welcome": "Hoş Geldiniz",
        "welcome_desc": "Gelişmiş derin öğrenme modelleri ile görüntü analizi yapın. Aşağıdaki alanlardan birini seçerek başlayın.",
        "select_domain": "Analiz Alanı Seçin",
        "analyze": "Analiz Et",
        "back_home": "← Ana Sayfaya Dön",
        "config": "⚙️ Yapılandırma",
        "select_arch": "Mimari Seçin:",
        "classes_supported": "sınıf destekleniyor",
        "upload_analyze": "📤 Görüntü Yükle & Analiz Et",
        "choose_image": "Bir görüntü dosyası seçin",
        "input_image": "📷 Giriş Görüntüsü",
        "prediction_results": "🎯 Tahmin Sonuçları",
        "analyzing": "Görüntü analiz ediliyor...",
        "predicted_class": "Tahmin Edilen Sınıf:",
        "confidence": "Güven Skoru",
        "view_probabilities": "📊 Tüm Sınıf Olasılıklarını Görüntüle",
        "feedback": "💬 Geri Bildirim",
        "feedback_desc": "Tahmin doğru muydu?",
        "correct": "✅ Doğru",
        "incorrect": "❌ Yanlış",
        "select_correct_class": "Doğru sınıfı seçin:",
        "submit_feedback": "Geri Bildirimi Gönder",
        "thank_you": "Teşekkür ederiz!",
        "feedback_recorded": "Geri bildirim kaydedildi",
        "feedback_submitted": "✓ Geri bildirim gönderildi",
        "no_model": "❌ Model dosyası bulunamadı!",
        "dl": "Derin Öğrenme",
        "tl": "Transfer Öğrenme",
        "how_to_use": "📖 Nasıl Kullanılır?",
        "step1": "1️⃣ Analiz etmek istediğiniz alanı seçin",
        "step2": "2️⃣ Model mimarisini seçin (DL veya TL)",
        "step3": "3️⃣ Görüntünüzü yükleyin",
        "step4": "4️⃣ Sonuçları inceleyin ve geri bildirim verin",
        "about": "ℹ️ Hakkında",
        "about_desc": "Bu platform, derin öğrenme ve transfer öğrenme tekniklerini kullanarak görüntü sınıflandırması yapar. Her model özel veri setleri ile eğitilmiştir."
    },
    "en": {
        "title": "🎯 AI Vision Platform",
        "subtitle": "Deep Learning & Transfer Learning",
        "welcome": "Welcome",
        "welcome_desc": "Analyze images using advanced deep learning models. Select one of the domains below to get started.",
        "select_domain": "Select Analysis Domain",
        "analyze": "Analyze",
        "back_home": "← Back to Home",
        "config": "⚙️ Configuration",
        "select_arch": "Select Architecture:",
        "classes_supported": "classes supported",
        "upload_analyze": "📤 Upload & Analyze Image",
        "choose_image": "Choose an image file",
        "input_image": "📷 Input Image",
        "prediction_results": "🎯 Prediction Results",
        "analyzing": "Analyzing image...",
        "predicted_class": "Predicted Class:",
        "confidence": "Confidence Score",
        "view_probabilities": "📊 View All Class Probabilities",
        "feedback": "💬 Feedback",
        "feedback_desc": "Was the prediction correct?",
        "correct": "✅ Correct",
        "incorrect": "❌ Incorrect",
        "select_correct_class": "Select the correct class:",
        "submit_feedback": "Submit Feedback",
        "thank_you": "Thank you!",
        "feedback_recorded": "Feedback recorded",
        "feedback_submitted": "✓ Feedback submitted",
        "no_model": "❌ No model files found!",
        "dl": "Deep Learning",
        "tl": "Transfer Learning",
        "how_to_use": "📖 How to Use?",
        "step1": "1️⃣ Select the domain you want to analyze",
        "step2": "2️⃣ Choose model architecture (DL or TL)",
        "step3": "3️⃣ Upload your image",
        "step4": "4️⃣ Review results and provide feedback",
        "about": "ℹ️ About",
        "about_desc": "This platform performs image classification using deep learning and transfer learning techniques. Each model is trained on specialized datasets."
    }
}

# --- MODEL KONFIGÜRASYONU ---
MODEL_CONFIG = {
    "Augmented Grapevine Disease": {
        "dl_path": "AugmentedGrapevineDisease/model_dl_grapevine_disease.keras",
        "tl_path": "AugmentedGrapevineDisease/model_tl_grapevine_disease.keras",
        "classes": ["Black Measles", "Black Rot", "Healthy", "Leaf Blight"],
        "icon": "🍇",
        "description_tr": "Üzüm hastalıklarını tespit eder",
        "description_en": "Detects grapevine diseases"
    },
    "Date Fruit Image": {
        "dl_path": "DateFruitImage/model_dl_date_fruit_image.keras",
        "tl_path": "DateFruitImage/model_tl_date_fruit_image.keras",
        "classes": ["Ajwa", "Galaxy", "Medjool", "Meneifi", "Nabtat Ali", "Rutab", "Shaishe", "Sokari", "Sugaey"],
        "icon": "🌴",
        "description_tr": "Hurma çeşitlerini sınıflandırır",
        "description_en": "Classifies date fruit varieties"
    },
    "Fish Species": {
        "dl_path": "FishSpecies/dl_model_fish_species.keras",
        "tl_path": None,
        "classes": ["Black Sea Sprat", "Gilt-Head Bream", "Hourse Mackerel", "Red Mullet", "Red Sea Bream", "Sea Bass", "Shrimp", "Striped Red Mullet", "Trout"],
        "icon": "🐟",
        "description_tr": "Balık türlerini tanır",
        "description_en": "Identifies fish species"
    },
    "Rice Image": {
        "dl_path": None,
        "tl_path": "RiceImage/tl_model_rice_image.keras",
        "classes": ["Arborio", "Basmati", "Ipsala", "Jasmine", "Karacadag"],
        "icon": "🍚",
        "description_tr": "Pirinç çeşitlerini ayırt eder",
        "description_en": "Distinguishes rice varieties"
    }
}

# --- DİĞER SABİTLER ---
FEEDBACK_DIR = "feedback_data"
