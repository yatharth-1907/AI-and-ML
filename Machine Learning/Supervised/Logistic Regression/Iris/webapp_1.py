import streamlit as st
import joblib 
import numpy as np
from sklearn.datasets import load_iris

model= joblib.load('iris_model.pkl')
iris= load_iris()

st.title("Iris Flower Prediction")

st.write("Adjust the Slider to predict the Iris Flower type.")

#Slider
sepal_length= st.slider("Sepal Length (cam)", 0.0,8.0,5.1)
sepal_width= st.slider("Sepal width (cam)", 0.0,8.0,5.1)
petal_length= st.slider("Petal Length (cam)", 0.0,8.0,5.1)
petal_width= st.slider("Petal width (cam)", 0.0,8.0,5.1)

#button
if st.button("Predict"):
    sample=np.array([
        sepal_length,
        sepal_width,
        petal_length,
        petal_width
    ]).reshape(1,-1)
    
    prediction= model.predict(sample)
    flower= iris.target_names[prediction[0]]
    
    st.success(f"Predicted flower:**{flower.capitalize()}**")