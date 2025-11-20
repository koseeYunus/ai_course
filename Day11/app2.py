import streamlit as st
import pickle

st.title("Maaş Tahmin Uygulaması")
st.subheader("Tecrübe, Yazılı Sınav ve Mülakat Puanına Göre Maaş Tahmini")

model = pickle.load(open('maas.pkl', 'rb'))

tecrube = st.number_input("Tecrübe (Yıl):", 1, 10)
yazili = st.number_input("Yazılı Sınav Puanı:", 1, 10)
mulakat = st.number_input("Mülakat Puanı:", 1, 10)

if st.button("Maaşı Tahmin Et"):
    tahmin = model.predict([[tecrube, yazili, mulakat]])
    tahmin = round(tahmin[0][0])
    st.success(f"Tahmin Edilen Maaş: {tahmin} TL")