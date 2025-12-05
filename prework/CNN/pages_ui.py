"""
Sayfa render fonksiyonları
"""
import streamlit as st
from PIL import Image
import os
from utils import load_model_file, preprocess_image, save_feedback, get_text
from config import MODEL_CONFIG


def render_home(translations, language):
    """Ana sayfa"""
    # Sağ üstte dil seçici
    col1, col2 = st.columns([5, 1])
    with col1:
        st.title(get_text(translations, language, "title"))
        st.caption(get_text(translations, language, "subtitle"))
    with col2:
        lang_options = {"English": "en", "Türkçe": "tr"}
        selected_lang = st.selectbox("🌐", options=list(lang_options.keys()), 
                                     index=list(lang_options.values()).index(language),
                                     label_visibility="collapsed")
        if lang_options[selected_lang] != language:
            st.session_state.language = lang_options[selected_lang]
            st.rerun()
    
    st.divider()
    
    # Hoş geldiniz bölümü
    st.header(get_text(translations, language, "welcome"))
    st.write(get_text(translations, language, "welcome_desc"))
    
    st.write("")
    
    # Nasıl kullanılır bölümü
    with st.expander(get_text(translations, language, "how_to_use"), expanded=False):
        st.write(get_text(translations, language, "step1"))
        st.write(get_text(translations, language, "step2"))
        st.write(get_text(translations, language, "step3"))
        st.write(get_text(translations, language, "step4"))
    
    # Hakkında bölümü
    with st.expander(get_text(translations, language, "about"), expanded=False):
        st.write(get_text(translations, language, "about_desc"))
    
    st.write("")
    st.subheader(get_text(translations, language, "select_domain"))
    st.write("")
    
    # 2x2 ızgara düzeninde model kartları
    topics = list(MODEL_CONFIG.keys())
    
    row1 = st.columns(2, gap="large")
    for idx in range(2):
        with row1[idx]:
            topic = topics[idx]
            conf = MODEL_CONFIG[topic]
            with st.container(border=True):
                st.subheader(f"{conf['icon']} {topic}")
                desc_key = "description_tr" if language == "tr" else "description_en"
                st.caption(conf[desc_key])
                st.write(f"**{len(conf['classes'])}** {get_text(translations, language, 'classes_supported')}")
                if st.button(get_text(translations, language, "analyze"), key=f"btn_{idx}", use_container_width=True, type="primary"):
                    st.session_state.page = 'predict'
                    st.session_state.selected_topic = topic
                    st.session_state.feedback_given = False
                    st.session_state.incorrect_clicked = False
                    st.rerun()
    
    st.write("")
    
    row2 = st.columns(2, gap="large")
    for idx in range(2, 4):
        with row2[idx-2]:
            topic = topics[idx]
            conf = MODEL_CONFIG[topic]
            with st.container(border=True):
                st.subheader(f"{conf['icon']} {topic}")
                desc_key = "description_tr" if language == "tr" else "description_en"
                st.caption(conf[desc_key])
                st.write(f"**{len(conf['classes'])}** {get_text(translations, language, 'classes_supported')}")
                if st.button(get_text(translations, language, "analyze"), key=f"btn_{idx}", use_container_width=True, type="primary"):
                    st.session_state.page = 'predict'
                    st.session_state.selected_topic = topic
                    st.session_state.feedback_given = False
                    st.session_state.incorrect_clicked = False
                    st.rerun()


def render_prediction_page(translations, language, feedback_dir):
    """Tahmin sayfası"""
    topic = st.session_state.selected_topic
    conf = MODEL_CONFIG[topic]
    
    st.title(f"{conf['icon']} {topic}")
    desc_key = "description_tr" if language == "tr" else "description_en"
    st.caption(conf[desc_key])
    st.divider()
    
    # Ana düzen
    col_left, col_right = st.columns([1, 3], gap="large")
    
    with col_left:      
        if st.button(get_text(translations, language, "back_home"), use_container_width=True):
            st.session_state.page = 'home'
            st.session_state.selected_topic = None
            st.session_state.feedback_given = False
            st.session_state.incorrect_clicked = False
            st.rerun()
        
        st.write("")
        
        with st.container(border=True):
            st.subheader(get_text(translations, language, "config"))
            
            # Model seçimi
            available_models = []
            if conf['dl_path'] and os.path.exists(conf['dl_path']):
                available_models.append(get_text(translations, language, "dl"))
            if conf['tl_path'] and os.path.exists(conf['tl_path']):
                available_models.append(get_text(translations, language, "tl"))
            
            if not available_models:
                st.error(get_text(translations, language, "no_model"))
                return
            
            model_type = st.selectbox(get_text(translations, language, "select_arch"), available_models)
            
            # Model mimarisi değiştiğinde feedback'ı sıfırla
            if st.session_state.selected_model_type != model_type:
                st.session_state.selected_model_type = model_type
                st.session_state.feedback_given = False
                st.session_state.incorrect_clicked = False
            
            # Gerçek model yolunu belirle
            if model_type == get_text(translations, language, "dl"):
                model_path = conf['dl_path']
            else:
                model_path = conf['tl_path']
            
            st.info(f"📊 **{len(conf['classes'])}** {get_text(translations, language, 'classes_supported')}")

    with col_right:
        with st.container(border=True):
            st.subheader(get_text(translations, language, "upload_analyze"))
            st.caption(get_text(translations, language, "choose_image"))
            uploaded_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")

    if uploaded_file:
        # Yeni görsel yüklenirse feedback'ı sıfırla
        if st.session_state.last_uploaded_file != uploaded_file.name:
            st.session_state.last_uploaded_file = uploaded_file.name
            st.session_state.feedback_given = False
            st.session_state.incorrect_clicked = False
        
        st.divider()
        
        col_img, col_result = st.columns(2, gap="large")
        
        with col_img:
            with st.container(border=True):
                st.subheader(get_text(translations, language, "input_image"))
                image = Image.open(uploaded_file).convert('RGB')
                st.image(image, use_container_width=True)
        
        with col_result:
            with st.container(border=True):
                st.subheader(get_text(translations, language, "prediction_results"))
                
                with st.spinner(get_text(translations, language, "analyzing")):
                    model = load_model_file(model_path)
                    
                    if model:
                        processed_img = preprocess_image(image)
                        predictions = model.predict(processed_img, verbose=0)
                        
                        class_names = conf['classes']
                        predicted_idx = predictions[0].argmax()
                        predicted_class = class_names[predicted_idx]
                        confidence = float(predictions[0][predicted_idx]) * 100
                        
                        # Sonuçlar
                        st.success(f"**{get_text(translations, language, 'predicted_class')}** {predicted_class}")
                        
                        col_m1, col_m2 = st.columns(2)
                        with col_m1:
                            st.metric(get_text(translations, language, "confidence"), f"{confidence:.1f}%")
                        with col_m2:
                            st.metric("Model", model_type)
                        
                        st.write("")
                        
                        # Tüm tahminler
                        with st.expander(get_text(translations, language, "view_probabilities")):
                            for i, class_name in enumerate(class_names):
                                prob = float(predictions[0][i]) * 100
                                st.progress(prob / 100, text=f"{class_name}: {prob:.1f}%")
                        
                        # Geri bildirim
                        st.divider()
                        st.subheader(get_text(translations, language, "feedback"))
                        st.caption(get_text(translations, language, "feedback_desc"))
                        
                        if not st.session_state.feedback_given:
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button(get_text(translations, language, "correct"), use_container_width=True, type="primary", key="correct_btn"):
                                    save_feedback(image, topic, model_type, predicted_class, predicted_class, True, feedback_dir)
                                    st.session_state.feedback_given = True
                                    st.session_state.incorrect_clicked = False
                                    st.success(get_text(translations, language, "thank_you"))
                                    st.balloons()
                            with col2:
                                if st.button(get_text(translations, language, "incorrect"), use_container_width=True, key="incorrect_btn"):
                                    st.session_state.incorrect_clicked = True
                            
                            # Yanlış seçildi ise doğru sınıfı seçtir
                            if st.session_state.incorrect_clicked:
                                st.write("")
                                correct_class = st.selectbox(
                                    get_text(translations, language, "select_correct_class"),
                                    options=class_names,
                                    key="correct_class_selector"
                                )
                                if st.button(get_text(translations, language, "submit_feedback"), use_container_width=True, type="primary", key="submit_incorrect"):
                                    save_feedback(image, topic, model_type, predicted_class, correct_class, False, feedback_dir)
                                    st.session_state.feedback_given = True
                                    st.session_state.incorrect_clicked = False
                                    st.success(get_text(translations, language, "thank_you"))
                        else:
                            st.info(get_text(translations, language, "feedback_submitted"))
