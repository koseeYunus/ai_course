import streamlit as st  
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

model=load_model('tl_skin_cancer_model.h5')
def process_image(img):
    img=img.resize((170,170))
    img=np.array(img)
    img=img/255.0 
    img=np.expand_dims(img,axis=0)
    return img
st.title('Deri Kanser resmi sınıflandırma :cancer:')
st.write('Resim seç, model kanser olup olmadığını tahmin etsin!')
file=st.file_uploader('Bir resim yükle',type=['jpg','jpeg','png'])
if file is not None: # Resim yuklenmisse burasi calisacak
    img=Image.open(file)
    st.image(img, caption='Yuklenen Resim')
    image=process_image(img)
    prediction=model.predict(image)
    predicted_class = 1 if prediction > 0.5 else 0
    class_names=['Kanser değil','Kanser']
    st.write(class_names[predicted_class])