import streamlit as st 
import requests

st.title("API Connect Iris Flower Prediction")

st.write("Enter Flower Measurement:")

#Slider
sepal_length = st.slider("Sepal Length",0.0, 10.0,5.1)
sepal_width = st.slider("Sepal Width",0.0, 10.0,5.1)
petal_length = st.slider("Petal Length",0.0, 10.0,5.1)
petal_width = st.slider("Petal Width",0.0, 10.0,5.1)

api_url= "http://127.0.0.1:5000/predict"

if st.button("Predict"):
    payload = {
        "sepal_length":sepal_length,
        "sepal_width":sepal_width,
        "petal_length":petal_length,
        "petal_width":petal_width
    }  
    
    try: 
         response= requests.post(api_url,json=payload)
         
         if response.status_code == 200:
             result= response.json()
             st.success(f"Predicted Flower: **{result['flower_name']}**")
         else:
             st.error("API error: unable to predict")
             
    except Exception as e:
        st.error (f"Connection error: {e}")
            
    