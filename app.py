from flask import Flask, render_template, request
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
    return "The learning page"

if __name__ == '__main__':
    app.run(debug=True)