import json
from flask import Flask, Response, request, render_template, redirect, url_for
import flask.ext.login as flask_lo
import urllib.request

app = Flask(__name__)


# Home Page
@app.route('/', methods=['GET'])
def home():
	return render_template('index.html')


# Interactive Map
def get_crime_points():
	url = "http://datamechanics.io/data/pt0713_silnuext/proj3/static/map_to_points.geojson"
	response = urllib.request.urlopen(url).read().decode("utf-8")
	crimes = json.loads(response)['features']
	return crimes

def get_opti_point():
	url = "http://datamechanics.io/data/pt0713_silnuext/proj3/static/optimization.geojson"
	response = urllib.request.urlopen(url).read().decode("utf-8")
	opt = json.loads(response)['features']
	return opt

@app.route("/map", methods=["GET", "POST"])
def map():
	crimes = get_crime_points()
	opt = get_opti_point()

	if request.method == "GET":
		return render_template('map.html', crimes=crimes, opt=opt)
	else:
		crime = request.form.get('crime')
		optimal = request.form.get('opt')
		if crime == "ALL":
			return ender_template('map.html', crimes=crimes)
		elif optimal == "ALL":
			return ender_template('map.html', opt=opt)
		else:
			for c in crimes:
				if c['properties']['crime location'] == crime:
					crime_point = c

			for o in opt:
				if o['properties']['coordinates'] == optimal:
					opt_point = o

			return render_template('map.html', crimes=select_crime, opt=select_opt)


# Interactive Scatter Plot Graph
@app.route("/relation", methods=["GET", "POST"])
def relation():
	return render_template('relation.html')


if __name__ == '__namin__':
	app.run(debug=True)
		