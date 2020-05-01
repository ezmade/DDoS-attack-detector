import socket
import pickle
import csv
import datetime
import time
import pandas
from timeit import default_timer as timer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
mlp_live_iteration = 0
allowed_IP = ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4']


def SnifferForLinux():
    pass


def LiveLabelEncoding(data):  # same as LabelEncoding(), but use for realtime
    data = pandas.read_csv('LiveAnn.csv', delimiter=',')
    columnsToEncode = list(data.select_dtypes(include=['category', 'object']))
    print(columnsToEncode)
    le = LabelEncoder()
    for feature in columnsToEncode:
        try:
            data[feature] = le.fit_transform(data[feature])
            # print(data[feature])
        except:
            print('error ' + feature)
    return data

# similar to MLP(), used for real-time classification and not for training
def MLP_Live_predict(cap, modelname, mlp_live_iteration):

    data = pandas.read_csv('LiveAnn.csv', delimiter=',')  # reads CSV
    data = LiveLabelEncoding(data)
    print("Processing Data", "\n")
    print(data)
    X = data[['Highest Layer', 'Transport Layer', 'Source IP', 'Dest IP', 'Source Port',
              'Dest Port', 'Packet Length', 'Packets/Time']]  # Data used to train

    from sklearn.preprocessing import StandardScaler
    #scaler = StandardScaler()
    # scaler.fit(X)
    #X = scaler.transform(X)

    loaded_model = pickle.load(open(modelname, 'rb'))  # loads model
    # print("Model Coeffcients ", loaded_model.coefs_) # load model coefs

    lmlp = loaded_model

    predictions = lmlp.predict(X)  # preditcions made by model

    hostile = 0  # this block counts how many 'hostile' packets have been predicted by the model
    safe = 0
    for check in predictions:
        if check == 1:  # change to 0 to force ddos attack
            hostile += 1
        else:
            safe += 1
    print("Safe Packets: ", safe)
    print("Possible Hostile Packets: ", hostile)
    print(100 * hostile/(safe + hostile))
    print("\n")
    mlp_live_iteration += 1

    if hostile >= ((safe + hostile)/2):
        testwrite = open('log.txt', 'a+')
        testwrite.write('Attack Detected at: ')
        testwrite.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        testwrite.write('\n')
        testwrite.write('Packets collected: ')
        testwrite.write(str(safe + hostile))
        testwrite.write('\n')
        return ("Attack")
    else:
        testwrite = open('log.txt', 'a+')
        testwrite.write('Normal Activity Detected at: ')
        testwrite.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        testwrite.write('\n')
        testwrite.write('Packets collected: ')
        testwrite.write(str(safe + hostile))
        testwrite.write('\n \n')

        return mlp_live_iteration
    # print("Predictions")
    #print (predictions)
    #from sklearn.metrics import classification_report,confusion_matrix

    # print(confusion_matrix(y,predictions))
    # print(classification_report(y,predictions))


# allows the program to differentiate between ipv4 and ipv6, needed for correct parsing of packets
def get_ip_layer_name(pkt):
    for layer in pkt.layers:
        if layer._layer_name == 'ip':
            return 4
        elif layer._layer_name == 'ipv6':
            return 6

# creates/rewrites 'Live.csv' file with 30 second intervals- writes header row - goes through packets, writing a row to the csv for each packet


def csv_interval_gather(cap):
    start_time = time.time()
    with open('LiveAnn.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Highest Layer', 'Transport Layer', 'Source IP',
                             'Dest IP', 'Source Port', 'Dest Port', 'Packet Length', 'Packets/Time'])

        i = 0
        start = timer()
        for pkt in cap:
            end = timer()
            if (end - start < 30):
                try:
                    if pkt.highest_layer != 'ARP':
                        print("Packets Collected:", i)
                        if pkt.highest_layer != 'ARP':
                            ip = None
                            ip_layer = get_ip_layer_name(pkt)
                            if ip_layer == 4:
                                ip = pkt.ip
                                # ipv = 0 # target test
                                if pkt.transport_layer == None:
                                    transport_layer = 'None'
                                else:
                                    transport_layer = pkt.transport_layer
                            elif ip_layer == 6:
                                ip = pkt.ipv6
                                # ipv = 1 # target test
                            try:
                                if ip.src not in allowed_IP:
                                    ipcat = 1
                                else:
                                    ipcat = 0
                                filewriter.writerow([pkt.highest_layer, transport_layer, ipcat, ip.dst, pkt[pkt.transport_layer].srcport,
                                                     pkt[pkt.transport_layer].dstport, pkt.length, i/(time.time() - start_time)])
                                print("Time: ", time.time() - start_time)
                                i += 1
                            except AttributeError:
                                if ip.src not in allowed_IP:
                                    ipcat = 1
                                else:
                                    ipcat = 0
                                filewriter.writerow(
                                    [pkt.highest_layer, transport_layer, ipcat, ip.dst, 0, 0, pkt.length, i/(time.time() - start_time)])
                                print("Time: ", time.time() - start_time)
                                i += 1

                        else:
                            if pkt.arp.src_proto_ipv4 not in allowed_IP:
                                ipcat = 1
                            else:
                                ipcat = 0
                            arp = pkt.arp
                            filewriter.writerow([pkt.highest_layer, transport_layer, ipcat,
                                                 arp.dst_proto_ipv4, 0, 0, pkt.length, i/(time.time() - start_time)])
                            print("Time: ", time.time() - start_time)
                            i += 1
                except (UnboundLocalError, AttributeError) as e:
                    print(e)
            else:
                return


def int_names(int_guids):  # Looks up the GUID of the network interfaces found in the registry, then converts them into an identifiable format
    int_names = int_names = ['(unknown)' for i in range(len(int_guids))]
    # reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    # reg_key = winreg.OpenKey(
        # reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
    for i in range(len(int_guids)):
        try:
            pass
            # reg_subkey = winreg.OpenKey(reg_key, int_guids[i] + r'\Connection')
            # int_names[i] = winreg.QueryValueEx(reg_subkey, 'Name')[0]
        except FileNotFoundError:
            pass
    return int_names


def int_choice():  # allows the user to choose interface
    for i, value in enumerate(int_names(int)):
        print(i, value)
    print('\n')
    iface = input("Please select interface: >")
    # cap = pyshark.LiveCapture(interface=iface)
    # cap.sniff_continuously(packet_count=None)

    # return cap
    return 0


def LabelEncoding(data):
    data = pandas.read_csv('NewComb2.csv', delimiter=',')
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
        mlp = MLPClassifier(hidden_layer_sizes=(100, 100), activation='logistic',
                            solver='sgd', max_iter=50, verbose=True,
                            early_stopping=False, shuffle=True)

    data = pandas.read_csv(load_data, delimiter=',')
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
        pickle.dump(mlp, open(filename, "wb"))


def CSVDataCheck():
    pass


def menu():
    answer = True
    while answer:
        print("""
            1. Neural Network Trainer
            2. Data Check
            3. Live Neural Network
            4. Exit
            """)

        answer = input('What would you like to do? >')
        if answer == '1':
            MLP()
        elif answer == '2':
            CSVDataCheck()
        elif answer == '3':
            live = True
            cap = int_choice()
            modelName = input("Please input model: >")
            try:
                while live:
                    csv_interval_gather(cap)
                    if MLP_Live_predict(cap, modelName, mlp_live_iteration) == "Attack":
                        live = False
                        print("DDoS ATTACK HAS BEEN DETECTED! @ ",
                              datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                        MLP_Live_predict(
                            cap, modelName, mlp_live_iteration) == 0
            except KeyboardInterrupt as e:
                print(e)
        elif answer == '4':
            break


def main():
    # interface = netifaces.interfaces()
    # allowed_IP = ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4']
    # cap = pyshark.FileCapture('test.pcap') # For training
    menu()


if __name__ == '__main__':
    main()
