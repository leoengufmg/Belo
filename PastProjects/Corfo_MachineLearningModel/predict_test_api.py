import joblib
import pandas as pd
from flask import request, jsonify
from flask import Flask

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():

     # lectura y deserializacion del modelo de clasificacion
     model = joblib.load('knn_model.pkl')

     # lectura y deserializacion del escalador
     scaler = joblib.load('scaler_model.pkl')

     json_ = request.json
     
     X = pd.DataFrame(json_)
     X_sc = scaler.transform(X)

     prediction = model.predict(X_sc)

     return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
     app.run(port=8080)
     