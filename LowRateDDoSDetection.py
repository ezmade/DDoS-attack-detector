import winreg
import netifaces
import pickle
import csv
import pyshark
import datetime
import time
import pandas
from timeit import default_timer as timer
from sklearn.preprocessing import LabelEncoder

def main():
    interface = netifaces.interfaces()
    allowed_IP = ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4']
    #cap = pyshark.FileCapture('test.pcap') # For training
    def LoadModel():
        filename = input('Name of model? >')
        loaded_model = pickle.load(open(filename, 'rb'))
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
            mlp = MLPClassifier(hidden_layer_sizes=(100, 100), activation='logistic', max_iter=1000, verbose=True, tol=0.00000001, early_stopping = True, shuffle = True)
            
        data = pandas.read_csv(load_data, delimiter=',')
        data = LabelEncoding(data)
        
    def CSVDataCheck():
        pass
    
    def menu():
        answer = True
        while answer:
            print ("""
                1. Neural Network Trainer
                2. Data Check
                3. Visual Model
                4. Exit
                """)
            
            answer = input('What would you like to do? >')
            if answer == '1':
                MLP()
            elif answer == '2':
                CSVDataCheck()
            elif answer == '3':
                network = DrawNN([8, 100, 100, 1])
                network.draw()
            elif answer == '4':
                break;
                
if __name__=='__main__':
    main()