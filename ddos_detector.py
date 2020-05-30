from pandas import read_csv
from pickle import load, dump
from sklearn.preprocessing import LabelEncoder
from numpy import reshape


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


def predict_ddos_attack(model, data):
    #data = read_csv(f'Data/{filename}', delimiter=',')
    #data = label_encoding(data)

    try:
        features = data[['Highest Layer', 'Transport Layer', 'Source IP', 'Dest IP', 'Source Port',
                        'Dest Port', 'Packet Length', 'Packets/Time']]
    except:
        print('Incorrect columns of dataset')
        return -1

    prediction = model.predict(features.values.reshape(1, -1))

    return prediction