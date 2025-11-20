import streamlit as st
import textblob as TextBlob

st.title("Metin Analizi Uygulaması")

metin = st.text_area("Metin Girin ve ctrl+enter ile analizi başlatın:")

if metin:
    polarity = TextBlob.TextBlob(metin).sentiment.polarity
    if polarity > 0.1:
        st.success(f"Olumlu bir metin girdiniz! (Polarity: {polarity})")
    elif polarity < -0.1:
        st.error(f"Olumsuz bir metin girdiniz! (Polarity: {polarity})")
    else:
        st.warning(f"Nötr bir metin girdiniz! (Polarity: {polarity})")