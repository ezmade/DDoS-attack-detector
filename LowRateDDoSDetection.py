import netifaces
import pickle
import csv
import pyshark
import datetime
import time
import pandas
from timeit import default_timer as timer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split #Needed to split the data into the training and testing

def LabelEncoding(data):
    return 0

def LoadModel():
    filename = input('Name of model? >')
    loaded_model = pickle.load(open(filename, 'rb'))
    print(loaded_model.coefs_)
    print(loaded_model.loss_)
        
    return loaded_model    

def main():
    #interface = netifaces.interfaces()
    #allowed_IP = ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4']
    #cap = pyshark.FileCapture('test.pcap') # For training
    menu()

    def LabelEncoding(data):
        data = pandas.read_csv('TestingData.csv', delimiter=',')
        columnsToEncode = list(data.select_dtypes(include=['category', 'object']))
        # print(data.dtypes) # Prints each column d_type
        # print(columnsToEncode) # Prints categorical features
        
        le = LabelEncoder()
        for feature in columnsToEncode:
            try:
                data[feature] = le.fit_transform(data[feature])
                # print(data[feature])
            except:
                print('error' + feature)
        return data
            
    def MLP():
        load_data = input('Name of CSV file? >')
        isLoad = input('Load model? (y/n) >')
        if isLoad == 'y':
            mlp = LoadModel()
        else:
            from sklearn.neural_network import MLPClassifier
            mlp = MLPClassifier(hidden_layer_sizes=(100, 100), activation='logistic', max_iter=1000, verbose=True, tol=0.00000001, early_stopping = True, shuffle = True)
            
        data = pandas.read_csv(load_data, delimiter=',')
        data = LabelEncoding(data)

        X = data[['Highest Layer', 'Transport Layer', 'Source IP', 'Dest IP', 'Source Port', 'Dest Port', 'Packet Length', 'Packets/Time']] # Data used to train
        # print("Features: ", "\n", X)
        y = data['target'] #targets for the MLP
        # print("Targets: ", "\n", y)

        X_train, X_test, y_train, y_test = train_test_split(X, y)


        #TODO: 
        # FIX THIS PART AND READ ABOUT StandartScaler
        # https://issue.life/questions/40758562
        # https://machinelearningmastery.com/feature-selection-machine-learning-python/


        scaler = StandardScaler()
        scaler.fit(X_train)
        # X_train = scaler.transform(X_train)
        # X_test = scaler.transform(X_test)

    def CSVDataCheck():
        pass
    
    def menu():
        answer = True
        while answer:
            print ("""
                1. Neural Network Trainer
                2. Data Check
                3. Exit
                """)
            
            answer = input('What would you like to do? >')
            if answer == '1':
                MLP()
            elif answer == '2':
                CSVDataCheck()
            elif answer == '3':
                break
                
if __name__=='__main__':
    main()
