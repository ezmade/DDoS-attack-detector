import os
from flask import Flask, render_template, request

from ddos_detector import predict_ddos_attack
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
    return 'The about page'

@app.route('/learning')
def learning():
    return render_template('learning.html')

@app.route('/classification')
def classification():
    return render_template('classification.html')

@app.route('/classificate-data', methods=['POST'])
def classificate_data():
    file = request.files.get('file')
    try:
        prediction = predict_ddos_attack('DDoS-attack-detector\Model\AdamClassifier.sav', file)
        return str(prediction), 200
    except:
        return '',400

if __name__ == '__main__':
    app.run(debug=True)