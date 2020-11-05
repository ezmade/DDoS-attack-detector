import os
from flask import Flask, render_template, request

from ddos_detector import predict_ddos_attack
from app_components import get_files_from_root
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model/')
@app.route('/model/<model_id>')
def model(model_id=0):
    return render_template('model.html', model_id=model_id)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/learning', methods=['GET'])
def learning():
    models = get_files_from_root('ddos-attack-detector\\Model', '.sav')
    message = 'Выбери модель'
    return render_template('learning.html', models=models, message=message)

@app.route('/classification')
def classification():
    return render_template('classification.html')

@app.route('/classificate-data', methods=['POST'])
def classificate_data():
    file = request.files.get('file')
    try:
        prediction = predict_ddos_attack('ddos-attack-detector\\Model\\AdamClassifier.sav', file)
        return str(prediction[0]), 200
    except:
        return '',400

if __name__ == '__main__':
    app.run(debug=True)