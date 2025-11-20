import streamlit as st
from gtts import gTTS

st.title('Text to Speech Uygulaması')
metin = st.text_area("Metin Girin ve ctrl+enter ile sesi oluşturun:")

if metin:
    tts = gTTS(text=metin, lang='tr')
    tts.save("output.mp3")
    ses= open("output.mp3", "rb")
    st.audio(ses, format='audio/mp3')