from flask import Flask, request, jsonify
import joblib
import numpy as np
from sklearn.datasets import load_iris

#Get the model
model= joblib.load('iris_model.pkl')

app= Flask(__name__)

@app.route("/predict",methods=['POST'])
def predict():
    data= request.get_json()
    iris=load_iris()
    
    features= [ 
               data["sepal_length"],
               data["sepal_width"],
               data["petal_length"],
               data["petal_width"]
               ]
    sample= np.array(features).reshape(1,-1)
    
    prediction= model.predict(sample)
    
    result= {
        "predicted class":int(prediction[0]),
        "flower_name": iris.target_names[prediction[0]]
    }
    return jsonify({
        "predicted class":int(prediction[0]),
        "flower_name": iris.target_names[prediction[0]]
    })
    
if __name__== "__main__":
    app.run(debug=True)