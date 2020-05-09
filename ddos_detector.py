from pandas import read_csv
from pickle import load, dump
from timeit import default_timer as timer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report


def LabelEncoding(data):
    data = read_csv('NewComb2.csv', delimiter=',')
    columnsToEncode = list(data.select_dtypes(include=['category', 'object']))
    print(data.dtypes) # Prints each column d_type
    print(columnsToEncode) # Prints categorical features

    le = LabelEncoder()
    for feature in columnsToEncode:
        try:
            data[feature] = le.fit_transform(data[feature])
            print(data[feature])
        except:
            print('error' + feature)
    return data


def LoadModel():
    filename = input('Name of model? >')
    loaded_model = load(open(filename, 'rb'))
    print(loaded_model.coefs_)
    print(loaded_model.loss_)

    return loaded_model


def MLP():
    load_data = input('Name of CSV file? >')
    isLoad = input('Load model? (y/n) >')
    if isLoad == 'y':
        mlp = LoadModel()
    else:
        from sklearn.neural_network import MLPClassifier
        mlp = MLPClassifier(hidden_layer_sizes=(100, 100), activation='logistic',
                            solver='sgd', max_iter=50, verbose=True,
                            early_stopping=False, shuffle=True)

    data = read_csv(load_data, delimiter=',')
    data = data.sample(frac=1).reset_index(drop=True)
    data = LabelEncoding(data)

    X = data[['Highest Layer', 'Transport Layer', 'Source IP', 'Dest IP', 'Source Port',
              'Dest Port', 'Packet Length', 'Packets/Time']]  # Data used to train
    # print("Features: ", "\n", X)
    y = data['target']  # targets for the MLP
    # print("Targets: ", "\n", y)

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # TODO:
    # FIX THIS PART AND READ ABOUT StandartScaler
    # https://issue.life/questions/40758562
    # https://machinelearningmastery.com/feature-selection-machine-learning-python/

    # scaler = StandardScaler()
    # scaler.fit(X_train)
    # X_train = scaler.transform(X_train)
    # X_test = scaler.transform(X_test)

    # print(X_train)  # Training data (fatures)
    # print(X_test)  # Test data (features)

    start_time = timer()
    mlp.fit(X_train, y_train)  # fit is used to actually train the model
    print(mlp.predict(X_test))
    end_time = timer()
    time_taken = end_time - start_time
    predictions = mlp.predict(X_test)
    print("First 50 Predictions: ", "\n", mlp.predict(X_test)[0:50]) # Prints first 50 predictions
    print("First 50 Probabilities: ", "\n", mlp.predict_proba(X_test)[0:50]) # Prints first 50 probabilites
    print("Number of iterations: ", mlp.n_iter_, "\n")
    hostile = 0
    safe = 0
    for check in predictions:
        if check:
            hostile += 1
        else:
            safe += 1
    print("Safe Packets: ", safe)
    print("Hostile Packets: ", hostile)
    print("Time Taken: ", time_taken)
    print("Confusion Matrix: ", "\n",
          confusion_matrix(y_test, predictions), "\n")
    print("Classification Report: ", "\n",
          classification_report(y_test, predictions), "\n")

    ci = input("Do you want to see weights and intercepts? (y/n) >")
    if ci == "y":
        print("Model Coefficients (Weights): ", "\n", mlp.coefs_, "\n")
        print("Model Intercepts (Nodes): ", "\n", mlp.intercepts_, "\n")
    else:
        pass

    save = input("Do you want to save model? (y/n) >")
    if save == "y":
        filename = input("Filename for saving? >")
        dump(mlp, open(filename, "wb"))

def menu():
    answer = True
    while answer:
        print("""
            1. Neural Network Trainer
            2. Exit
            """)

        answer = input('What would you like to do? >')
        if answer == '1':
            MLP()
        elif answer == '2':
            break
