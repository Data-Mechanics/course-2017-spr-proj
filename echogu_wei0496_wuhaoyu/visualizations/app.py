# -*- coding: utf-8 -*-

import urllib.request
import json
from flask import Flask, jsonify, abort, make_response, request, render_template

app = Flask(__name__)

# Map
@app.route("/", methods=["GET", "POST"])
def map():
	schools = get_schools()
	schools_list = sorted([s['properties']['school'] for s in schools])
	routes = get_routes()
	yards = get_yards()

	if request.method == "GET":
		return render_template("index.html", routes=routes, schools=schools, yards=yards, schools_list=schools_list)
	else:
		school = request.form.get('school')

		if school == "All":
			return render_template("index.html", routes=routes, schools=schools, yards=yards, schools_list=schools_list)
		else:
			selected_routes = []
			selected_yards = []
			selected_schools = []
			for r in routes:
				if r['properties']['school'] == school:
					selected_routes.append(r)
					for y in yards:
						if r['properties']['yard'] == y['properties']['yard']:
							selected_yards.append(y)
			for s in schools:
				if s['properties']['school'] == school:
					selected_schools.append(s)
			return render_template("index.html", routes=selected_routes, schools=selected_schools, yards=selected_yards, schools_list=schools_list)

# extract route, school and yard info from geojson
def get_routes():
	url = "http://datamechanics.io/data/echogu_wei0496_wuhaoyu/routes.geojson"
	response = urllib.request.urlopen(url).read().decode("utf-8")
	routes = json.loads(response)['features']
	return routes

def get_yards():
	url = "http://datamechanics.io/data/echogu_wei0496_wuhaoyu/yards.geojson"
	response = urllib.request.urlopen(url).read().decode("utf-8")
	yards = json.loads(response)['features']
	return yards

def get_schools():
	url = "http://datamechanics.io/data/echogu_wei0496_wuhaoyu/schools.geojson"
	response = urllib.request.urlopen(url).read().decode("utf-8")
	schools = json.loads(response)['features']
	return schools

if __name__ == '__main__':
    app.run(debug=True)
