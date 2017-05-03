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

def list_crime():
	crimes = get_crimes()['features']
	crimes_list = [s['properties']['crime'] for s in crimes]
	return render_template("map.html", crimes=crimes_list)

def one_optimization():
	optimization = get_crimes()['features']
	optimization_list = [s['properties']['crime'] for s in optimization]
	return render_template("map.html", optimization = optimization_list)

def select_crime():
	crime = request.form.get("crime")
	routes = get_routes()['features']
	selected_crime = []
	for r in routes:
		if r['properties']['crime'] == crime:
			selected_crime.append(r)
	print(selected_crime)
	return render_template("map.html", route=selected_crime)

def select_optimization():
	optimization = request.form.get("optimization")
	routes = get_routes()['features']
	selected_optimization = []
	for r in routes:
		if r['properties']['optimization'] == optimization:
			selected_optimization.append(r)
	print(selected_optimization)
	return render_template("map.html", route=selected_optimization)


if __name__ == '__main__':
    app.run(debug=True)
