import streamlit as st
import ollama
import base64
from PIL import Image
import io
import time

st.set_page_config(page_title="OCR Extractor", page_icon="📄", layout="centered")

st.title("📄 AI Powered Image Text Extractor")
st.write("Bir resim yükleyin ve yapay zeka içindeki metni çıkartsın.")

uploaded_file = st.file_uploader("Bir resim seçin:", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Yüklenen Görsel", use_container_width=True)

    if st.button("📤 Metni Çıkart"):
        st.info("Görsel işleniyor... Lütfen bekleyin.")

        # progress bar
        progress = st.progress(0)
        status_text = st.empty()

        # simulate progress bar (UI effect)
        for pct in range(0, 60, 10):
            progress.progress(pct)
            status_text.write(f"🧠 Yapay zeka görseli analiz ediyor... %{pct}")
            time.sleep(0.2)

        try:
            # base64 encode
            image_bytes = uploaded_file.getvalue()
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")

            status_text.write("🔍 Metin çıkartılıyor...")

            res = ollama.chat(
                model="llama3.2-vision:latest",
                messages=[
                    {
                        "role": "user",
                        "content": "extract text from this image, no comments, just written text",
                        "images": [image_b64],
                    }
                ],
            )

            progress.progress(100)
            status_text.write("✅ İşlem tamamlandı!")

            st.success("Metin başarıyla çıkarıldı!")
            st.subheader("📌 Çıkarılan Metin:")
            st.write(res["message"]["content"])

        except Exception as e:
            st.error("❌ Bir hata oluştu:")
            st.error(str(e))
