import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from ddos_detector import predict_ddos_attack
from model_fitting import  ACTIVATIONS, SOLVERS, label_encoding
from app_components import get_files_from_root
from pandas import read_csv
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, f1_score, average_precision_score
from forms import ClassificationForm, LearningForm

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/model')
@app.route('/model/<model_id>')
def model(model_id=0):
    return render_template('model.html', model_id=model_id)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/learning', methods=['GET', 'POST'])
def learning():
    form = LearningForm()
    form.activations.choices = ACTIVATIONS
    form.solvers.choices = SOLVERS
    success = False
    accuracy = "Accuracy: "
    precision = "Precision: "
    f1score = "F1-Score: "
    if form.validate_on_submit():
        activation = form.activations.data
        solver = form.solvers.data
        if form.max_iters.data:
            max_iter = int(form.max_iters.data)
        else:
            max_iter = 5
        if form.sizes.data:
            sizes = (int(form.sizes.data), int(form.sizes.data))
        else:
            sizes = (10, 10)
        try:
            accuracy, precision, f1score = MLP(sizes, activation, solver, max_iter)
            success = True
        except Exception as e:
            print(e)
            return str(e), 400

    return render_template(
        'learning.html', 
        form=form,
        success=success,
        accuracy=accuracy,
        precision=precision,
        f1score=f1score
        )


@app.route('/classification', methods=['GET', 'POST'])
def classification():
    form = ClassificationForm()
    models = get_files_from_root('./models', '.sav')
    form.classification_model.choices=models
    data = []
    predictions = []
    length = 0
    if form.validate_on_submit():
        input_file = f'data/{form.input_file.data}'
        modelname = form.classification_model.data
        try:
            data, predictions = predict_ddos_attack(f'models/{modelname}', input_file)
            length = len(predictions)
        except:
            return 'Something goes wrong! Try again', 400
    return render_template(
        'classification.html', 
        form = form, 
        data = data,
        predictions = predictions, 
        length = length
        )


def MLP(sizes, activation, solver, max_iter):
    load_data = "NewComb2.csv"
    from sklearn.neural_network import MLPClassifier
    mlp = MLPClassifier(hidden_layer_sizes=sizes, activation=activation,
                        solver=solver, max_iter=max_iter, verbose=True,
                        early_stopping=False, shuffle=True)

    data = read_csv(f'data/{load_data}', delimiter=',')
    data = data.sample(frac=1).reset_index(drop=True)
    encoded_data = label_encoding(data)

    X = encoded_data[['Highest Layer', 'Transport Layer', 'Source IP', 'Dest IP', 'Source Port',
                        'Dest Port', 'Packet Length', 'Packets/Time']]
    y = encoded_data['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    mlp.fit(X_train, y_train)  # fit is used to actually train the model
    predictions = mlp.predict(X_test)
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

    return acc, prec, f1
if __name__ == '__main__':
    app.run(debug=True)