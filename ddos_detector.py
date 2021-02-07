from pandas import read_csv
from pickle import load, dump
from sklearn.preprocessing import LabelEncoder
from numpy import reshape


def label_encoding(data):
    columns_to_encode = list(data.select_dtypes(include=['category', 'object']))
    le = LabelEncoder()
    for feature in columns_to_encode:
        try:
            data[feature] = le.fit_transform(data[feature])
        except:
            print('error' + feature)
    return data


def load_model(path):
    with open(path, "rb") as f:
        try:
            loaded_model = load(f)
        except:
            print('Somethind wrong with the input file.')
    return loaded_model


def predict_ddos_attack(model_path, file):
    model = load_model(model_path)
    data = read_csv(file)
    enconded_data = label_encoding(data)
    try:
        features = enconded_data[['Highest Layer', 'Transport Layer', 'Source IP', 'Dest IP', 'Source Port',
                        'Dest Port', 'Packet Length', 'Packets/Time']]
    except:
        print('Incorrect columns of dataset')
        return -1
    
    prediction = model.predict(features)
    return prediction