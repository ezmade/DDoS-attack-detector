from pandas import read_csv
from pickle import load, dump
from timeit import default_timer as timer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report


def label_encoding(data):
    columns_to_encode = list(data.select_dtypes(include=['category', 'object']))
    print(data.dtypes) # Prints each column d_type
    print(columns_to_encode) # Prints categorical features

    le = LabelEncoder()
    for feature in columns_to_encode:
        try:
            data[feature] = le.fit_transform(data[feature])
            print(data[feature])
        except:
            print('error' + feature)
    return data


def load_model(filename):
    loaded_model = load(open(f'Model/{filename}', 'rb'))
    print(loaded_model.coefs_)
    print(loaded_model.loss_)

    return loaded_model


def predict_ddos_attack(modelname, filename):
    model = load_model(modelname)
    data = read_csv(f'Data/{filename}', delimiter=',')
    data = label_encoding(data)

    features = data[['Highest Layer', 'Transport Layer', 'Source IP', 'Dest IP', 'Source Port',
              'Dest Port', 'Packet Length', 'Packets/Time']]
    
    predictions = model.predict(features)

    return predictions