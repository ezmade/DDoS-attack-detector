import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from ddos_detector import predict_ddos_attack
from model_fitting import  ACTIVATIONS, SOLVERS, MLP
from app_components import get_files_from_root
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
    if form.validate_on_submit():
        activation = form.activations.data
        solver = form.solvers.data
        if form.max_iters.data:
            max_iter = form.max_iters.data
        else:
            max_iter = 5
        if form.sizes.data:
            sizes = (int(form.sizes.data), int(form.sizes.data))
        else:
            sizes = (10, 10)
        try:
            MLP(sizes, activation, solver, max_iter)
            success = True
        except:
            return 'Something goes wrong! Try again', 400
    return render_template(
        'learning.html', 
        form=form,
        success=success
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


if __name__ == '__main__':
    app.run(debug=True)