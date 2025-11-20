import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title('Image to Sketch')
file=st.file_uploader('upload a portrait Image', type=['jpg','png','jpeg'])
if file:
    img=Image.open(file).convert('RGB')
    img2=np.array(img)
    img_bw=cv2.cvtColor(img2,cv2.COLOR_RGB2BGR)
    gray=cv2.cvtColor(img_bw,cv2.COLOR_RGB2GRAY)
    inverted=255-gray
    blurred=cv2.GaussianBlur(inverted,(21,21),0)
    
    def dodge(front,back):
        return cv2.divide(front, 255-back, scale=255)
        
    sketch=dodge(gray,blurred)
    
    st.subheader('Original vs Sketch')
    col1,col2=st.columns(2)
    with col1:
        st.image(img, caption='Original', use_container_width=True)
    with col2:
        st.image(sketch, caption='Sketch', use_container_width=True)