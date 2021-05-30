from pandas import read_csv
from timeit import default_timer as timer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, f1_score, average_precision_score
import tensorflow as tf
import numpy as np


ACTIVATIONS = ['relu', 'logistic', 'identity', 'tanh']
SOLVERS = ['lbfgs', 'sgd', 'adam']


def label_encoding(data):
    columns_to_encode = list(data.select_dtypes(include=['category', 'object']))
    le = LabelEncoder()
    for feature in columns_to_encode:
        try:
            data[feature] = le.fit_transform(data[feature])
        except:
            print('error' + feature)
    return data


def MLP(sizes, activation, solver, max_iter, dataset, label_name):
    load_data = dataset
    from sklearn.neural_network import MLPClassifier
    mlp = MLPClassifier(hidden_layer_sizes=sizes, activation=activation,
                        solver=solver, max_iter=max_iter, verbose=True,
                        early_stopping=False, shuffle=True)
    data = read_csv(load_data, delimiter=',')
    data = data.sample(frac=1).reset_index(drop=True)
    encoded_data = label_encoding(data)
    y = encoded_data[label_name]
    X = encoded_data.drop(label_name, axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    start_time = timer()
    mlp.fit(X_train, y_train)  # fit is used to actually train the model
    end_time = timer()
    time_taken = end_time - start_time
    predictions, predictions_proba = mlp.predict(X_test), mlp.predict_proba(X_test)
    print("Number of iterations: ", mlp.n_iter_, "\n")
    hostile = 0
    safe = 0
    for check in predictions:
        if check:
            hostile += 1
        else:
            safe += 1
    acc = accuracy_score(y_test, predictions)
    prec = average_precision_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    class_report = classification_report(y_test, predictions)
    print("Safe Packets: ", safe)
    print("Hostile Packets: ", hostile)
    print("Classification Report: ", "\n",class_report, "\n")

    # ci = input("Do you want to see weights and intercepts? (y/n) >")
    # if ci == "y":
    # print("Model Coefficients (Weights): ", "\n", mlp.coefs_, "\n")
    # print("Model Intercepts (Nodes): ", "\n", mlp.intercepts_, "\n")
    # else:
    #     pass

    # save = input("Do you want to save model? (y/n) >")
    # if save == "y":
    #     filename = input("Filename for saving? >")
    #     dump(mlp, open(filename, "wb"))

    return acc, prec, f1, y_test, predictions_proba, time_taken
    

def predict_ddos_attack(model_name, file):
    model = tf.keras.models.load_model(f'models/{model_name}')
    data = read_csv(file)
    features = label_encoding(data.drop(columns='Label'))
    features.replace([np.inf, -np.inf], np.nan, inplace=True)
    for col in features.select_dtypes(include=np.number):
        features[col] = features[col].fillna(features[col].median())
    prediction = model.predict(features)
    prediction = np.argmax(prediction, axis = 1)
    return data, prediction