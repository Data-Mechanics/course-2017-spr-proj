import jsonschema
import json
from flask import Flask, jsonify, abort, make_response, request, render_template
# from flask.ext.httpauth import HTTPBasicAuth
# from flask import Flask, Response, request, render_template, redirect,
# import flask.ext.login as flask_login

app = Flask(__name__)
# auth = HTTPBasicAuth()

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Map
@app.route("/map", methods=["GET"])
def list_schools():
	schools = get_schools()['features']
	schools_list = [s['properties']['school'] for s in schools]
	return render_template("map.html", schools=schools_list)

@app.route("/map", methods=["POST"])
def select_school():
	school = request.form.get("school")
	routes = get_routes()['features']
	selected_routes = []
	for r in routes:
		if r['properties']['school'] == school:
			selected_routes.append(r)
	print(selected_routes)
	return render_template("map.html", route=selected_routes)

def get_routes():
	routes = json.load(open('static/route.geojson', 'r'))
	return routes

def get_schools():
	schools = json.load(open('static/schools.geojson', 'r'))
	return schools

def get_yards():
	yards = json.load(open('static/schools.geojson', 'r'))
	return yards
	

if __name__ == '__main__':
    app.run(debug=True)
