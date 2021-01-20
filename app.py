import os
from flask import Flask, render_template, request
from ddos_detector import predict_ddos_attack
from app_components import get_files_from_root
from forms import ClassificationForm

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/model/<model_id>')
def model(model_id=0):
    return render_template('model.html', model_id=model_id)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/learning', methods=['GET'])
def learning():
    models = get_files_from_root('./models', '.sav')
    return render_template('learning.html', models=models)


@app.route('/classification')
def classification():
    form = ClassificationForm()
    models = get_files_from_root('./models', '.sav')
    form.classification_model.choices=models
    return render_template('classification.html', models=models, form=form)


@app.route('/classificate-data', methods=['POST'])
def classificate_data():
    file = request.files.get('file')
    model = request.values.get('modelname')
    print(model, str(file))
    try:
        prediction = predict_ddos_attack(f'./models/{model}', file)
        print(str(prediction[0]))
        return str(prediction[0]), 200
    except:
        return '',400


if __name__ == '__main__':
    app.run(debug=True)