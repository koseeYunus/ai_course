import streamlit as st
import pandas as pd
import plotly.express as px

st.title("MLOps Streamlit App")
st.header("Maas Tahmin Uygulamasi")

df=pd.read_csv("prog_languages_data.csv")
st.dataframe(df)

fig=px.pie(df, values="Sum")
st.plotly_chart(fig)

fig2=px.bar(df, x='lang', y='Sum')
st.plotly_chart(fig2)


# st.title("MLOps Streamlit App :balloon:")
# st.header("Welcome to the MLOps Streamlit Application!")
# st.subheader("This is a simple demonstration of Streamlit capabilities.")
# st.text("This is a sample text to show how Streamlit works.")
# st.text_area("Enter some text here:", "Type your text...")
# st.number_input("Enter a number:", min_value=0, max_value=100, value=50)
# st.slider("Select a range of values:", 0, 100, (25, 75))
# st.selectbox("Choose an option:", ["Option 1", "Option 2", "Option 3"])
# st.multiselect("Select multiple options:", ["Option A", "Option B", "Option C"])
# st.checkbox("Check me out!")
# st.radio("Pick one:", ["Choice 1", "Choice 2", "Choice 3"])
# st.button("Click Me!")
# st.file_uploader("Upload a file:")
# st.color_picker("Pick a color:", "#00f900")
# st.progress(70)
# st.balloons()
# st.date_input("Select a date")
# st.time_input("Select a time")
# st.camera_input("Take a picture")
# st.image("image_02.jpg")
# st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
# st.video("secret_of_success.mp4")
# calsitirmak icin streamlit run app1.py
