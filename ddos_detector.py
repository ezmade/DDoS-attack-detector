from pandas import read_csv
from pickle import load, dump
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import numpy as np


def label_encoding(data):
    columns_to_encode = list(data.select_dtypes(include=['category', 'object']))
    le = LabelEncoder()
    for feature in columns_to_encode:
        try:
            data[feature] = le.fit_transform(data[feature])
        except:
            print('error' + feature)
    return data


# def load_model(path):
#     with open(path, "rb") as f:
#         try:
#             loaded_model = load(f)
#         except:
#             print('Somethind wrong with the input file.')
#     return loaded_model


def predict_ddos_attack(model_name, file):
    print(model_name)
    model = tf.keras.models.load_model(f'models/{model_name}')
    print('1')
    data = read_csv(file)
    print('2')
    features = label_encoding(data.drop(columns='Label'))
    print('3')
    features.replace([np.inf, -np.inf], np.nan, inplace=True)
    print('4')
    for col in features.select_dtypes(include=np.number):
        features[col] = features[col].fillna(features[col].median())
    
    print('okay')
    prediction = model.predict(features)
    prediction = np.argmax(prediction, axis = 1)
    return data, prediction