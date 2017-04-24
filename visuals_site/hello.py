from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)
from visual1data import VisualOne
import json

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/plot')
def visual_1_with_bounds():
	minimum = request.args.get('min')
	maximum = request.args.get('max')
	try:
		minimum = int(minimum)
	except (ValueError, TypeError):
		minimum = 0
	try:
		maximum = int(maximum)
	except (ValueError, TypeError):
		maximum = 100000
	data = VisualOne.get_data(minimum, maximum)
	return render_template('plot.html', minimum=minimum, maximum=maximum, data=json.dumps(data))

@app.route('/map')
def map():
	return render_template('map.html')
