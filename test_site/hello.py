from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Index Page'

@app.route('/hello/<int:parameter>')
def hello(parameter):
	return render_template('index.html')
