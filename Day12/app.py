import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import streamlit as st

df=pd.read_excel('cars.xlsx')
x=df.drop('Price', axis=1)
y=df[['Price']]

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20, random_state=42)

preprocessor=ColumnTransformer(
    transformers=[
        ('num',StandardScaler(),['Mileage','Cylinder','Liter','Doors']),
        ('cat',OneHotEncoder(),['Make','Model','Trim','Type'])
    ]
)

model=LinearRegression()

pipeline=Pipeline(steps=[('preprocessor',preprocessor),('regressor',model)])
pipeline.fit(x_train,y_train)
pred=pipeline.predict(x_test)

r2=r2_score(y_test,pred)
rmse= mean_squared_error(y_test,pred)**0.5

def price_pred(make,model,trim,mileage,type_,cylinder,liter,doors,cruise,sound,leather):
    input_data=pd.DataFrame({
        'Make':[make],
        'Model':[model],
        'Trim':[trim],
        'Mileage':[mileage],
        'Type':[type_],
        'Cylinder':[cylinder],
        'Liter':[liter],
        'Doors':[doors],
        'Cruise':[cruise],
        'Sound':[sound],
        'Leather':[leather],
    })
    
    prediction=pipeline.predict(input_data)[0]
    return prediction

st.title("MLOps Car Price Prediction App :red_car:")
st.write("Enter the car details to predict the price")

make=st.selectbox("Make", df['Make'].unique())
carmodel=st.selectbox("Model", df[df['Make']==make]['Model'].unique())
trim=st.selectbox("Trim", df[df['Model']==carmodel]['Trim'].unique())
mileage=st.number_input("Mileage", min_value=2000, max_value=200000, value=50000, step=1000)
car_type=st.selectbox("Type", df['Type'].unique())
cylinder=st.selectbox("Cylinder", sorted(df['Cylinder'].unique()))
liter=st.number_input("Liter", min_value=1, max_value=6, value=2, step=1)
doors=st.selectbox("Doors", df['Doors'].unique())
cruise=st.radio("Cruise", ('Yes', 'No')) == 'Yes'
sound=st.radio("Sound System", ('Yes', 'No')) == 'Yes'
leather=st.radio("Leather Seats", ('Yes', 'No')) == 'Yes'

if st.button("Predict"):
    predicted_price=price_pred(make, carmodel, trim, mileage, car_type, cylinder, liter, doors, cruise, sound, leather)
    price=float(predicted_price)
    st.success(f"The predicted price of the car is: ${price:,.2f}")
    st.write(f"Model R² Score: {r2:.2f}")
    st.write(f"Model RMSE: {rmse:,.2f}")

    new = pd.DataFrame([{
        'Price':price, 'Make': make, 'Model': carmodel, 'Trim': trim, 'Mileage': mileage,
        'Type': car_type, 'Cylinder': cylinder, 'Liter': liter, 'Doors': doors,
        'Cruise': cruise, 'Sound': sound, 'Leather': leather
        }])
    st.write(new)
    st.write(df.shape)
    updated = pd.concat([df, new], ignore_index=True)
    st.write(updated.shape)
    updated.to_excel('cars.xlsx', index=False)
