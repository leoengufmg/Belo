import joblib
import pandas as pd
from flask import request, jsonify
from flask import Flask

app = Flask(__name__)


def predict():
    global model
    global scaler
    # lectura y deserializacion del modelo de clasificacion
    model = joblib.load('knn_model.pkl')
    # lectura y deserializacion del escalador
    scaler = joblib.load('scaler_model.pkl')
    print("Predictions: RGB (Red Giant Branch) or HeB (Helium Burning)")
    #user_input = int(input("0 to cancel and 1 to predict:  "))
    #while(user_input != 0):
    dnu = float(input("Ingrese valor de Dnu: "))
    print(dnu)
    numax = float(input("Ingrese valor de numax: "))
    print(numax)
    epsilon = float(input("Ingrese valor de epsilon: "))
    print(epsilon)
    p = [[dnu, numax, epsilon]]
    result = model.predict(p)
    #print(result[0])
    if(result[0]):
        print("Population class predictions for Kepler red giants: HeB (Helium Burning)")
    else:
        print("RGB (Red Giant Branch)")

if __name__ == '__main__':
    predict()
