from pandas import read_csv
from pickle import load, dump
from sklearn.preprocessing import LabelEncoder
from numpy import reshape


def label_encoding(data):
    columns_to_encode = list(data.select_dtypes(include=['category', 'object']))
    # print(data.dtypes) # Prints each column d_type
    # print(columns_to_encode) # Prints categorical features

    le = LabelEncoder()
    for feature in columns_to_encode:
        try:
            data[feature] = le.fit_transform(data[feature])
            print(data[feature])
        except:
            print('error' + feature)
    return data


def load_model(path):
    loaded_model = load(open(path, 'rb'))
    # print(loaded_model.coefs_)
    # print(loaded_model.loss_)

    return loaded_model


def predict_ddos_attack(model_path, file):
    model = load_model(model_path)
    data = read_csv(file)
    enconded_data = label_encoding(data)
    try:
        print('good')
        features = enconded_data[['Highest Layer', 'Transport Layer', 'Source IP', 'Dest IP', 'Source Port',
                        'Dest Port', 'Packet Length', 'Packets/Time']]
        print(features)
    except:
        print('Incorrect columns of dataset')
        return -1
    print('good2')
    prediction = model.predict(features)
    print('good3')
    return prediction