from datetime import time
import os
from flask import Flask, render_template, request
from flask_bs4 import Bootstrap
from ddos_detector import predict_ddos_attack
from model_fitting import  ACTIVATIONS, SOLVERS, MLP
from app_components import get_files_from_root, allowed_file
from forms import ClassificationForm, LearningForm
from werkzeug.utils import secure_filename
import scikitplot as skplt
import matplotlib.pyplot as plt

UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/models')
def models():
    return render_template('models.html')


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
    time_taken = 0
    if form.validate_on_submit():
        activation = form.activations.data
        solver = form.solvers.data
        input_file = request.files['input_file']
        if input_file and allowed_file(input_file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(input_file.filename)
            input_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = f'data/{filename}'
        if form.max_iters.data:
            max_iter = int(form.max_iters.data)
        else:
            max_iter = 5
        if form.sizes.data:
            sizes = (int(form.sizes.data), int(form.sizes.data))
        else:
            sizes = (10, 10)
        try:
            accuracy, precision, f1score, y_test, y_proba, _, time_taken= MLP(sizes, activation, solver, max_iter, data)
            skplt.metrics.plot_roc(y_test, y_proba)
            plt.savefig('static/img/roc.png', dpi=512)
            success = True
            print(time_taken)
        except Exception as e:
            print(e)
            return str(e), 400

    return render_template(
        'learning.html', 
        form=form,
        success=success,
        accuracy=accuracy,
        precision=precision,
        f1score=f1score,
        time_taken=time_taken
        )


@app.route('/classification', methods=['GET', 'POST'])
def classification():
    form = ClassificationForm()
    models = get_files_from_root('./models', '.sav')
    form.classification_model.choices=models
    data = []
    predictions = []
    success = False
    error_found = False
    length = 0
    if form.validate_on_submit():
        input_file = request.files['input_file']
        if input_file and allowed_file(input_file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(input_file.filename)
            input_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        modelname = form.classification_model.data
        file = f'data/{filename}'
        try:
            data, predictions = predict_ddos_attack(f'models/{modelname}', file)
            length = len(predictions)
            success = True
        except:
            error_found = True
            return 'Something goes wrong! Try again', 400
    return render_template(
        'classification.html', 
        form=form, 
        data=data,
        predictions=predictions, 
        length=length,
        success=success,
        error_found=error_found
        )

if __name__ == '__main__':
    app.run(debug=True)