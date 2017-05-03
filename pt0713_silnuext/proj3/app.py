import json
from flask import Flask, Response, request, render_template, redirect, url_for
import flask.ext.login as flask_lo

app = Flask(__name__)


# Home Page
@app.route('/', methods=['GET'])
def home():
	return render_template('index.html')


# Interactive Map
def get_crime_points():
	crime_points = json.load(open('static/map_to_points.geojson', 'r'))
	return crime_points

def get_optimization_point():
	optimization_point = json.load(open('static/optimization.geojson', 'r'))
	return optimization_point
