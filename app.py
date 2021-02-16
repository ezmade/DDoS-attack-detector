import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from ddos_detector import predict_ddos_attack
from app_components import get_files_from_root
from forms import ClassificationForm
from bs4 import BeautifulSoup

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


@app.route('/learning', methods=['GET'])
def learning():
    models = get_files_from_root('./models', '.sav')
    return render_template('learning.html', models=models)


@app.route('/classification', methods=['GET', 'POST'])
def classification():
    form = ClassificationForm()
    models = get_files_from_root('./models', '.sav')
    form.classification_model.choices=models
    info = []
    if form.validate_on_submit():
        input_file = f'data/{form.input_file.data}'
        modelname = form.classification_model.data
        try:
            predictions = predict_ddos_attack(f'models/{modelname}', input_file)
            for i in range(0, 10):
                if predictions[i]==0:
                    info.append('Результат: OK')
                else:
                    info.append('Результат: Bad traffic')
        except:
            return 'Something goes wrong! Try again', 400
    return render_template('classification.html', form=form, info=info)


def insert_classification_info(page, info):
    with open(page, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, features='html.parser')
        result = soup.new_tag('p')
        result.string = info
        tag = soup.find('p', attrs={'id' : 'result'})
        tag.insert(new_tag)


if __name__ == '__main__':
    app.run(debug=True)