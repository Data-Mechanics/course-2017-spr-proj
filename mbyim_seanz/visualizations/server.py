from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/propertyClusterLeaflet', methods=['GET'])
def propertyClusterLeaflet():
    return render_template('propertyClusterLeaflet.html')

@app.route('/residentialYearsBarChart', methods=['GET'])
def residentialYearsBar():
    return render_template('residentialYearsBarChart.html')

@app.route('/assessedProperty')
def getAssessedProperty():
	'''returns geojson object of all assessed property '''
	assessed_prop = json.load(open('json/assessed_prop.geojson','r'))
	return jsonify(assessed_prop)

@app.route('/neighborhoods')
def getNeighborhoods():
	'''returns geojson object of all neighborhoods in Boston'''
	neighborhoods = json.load(open('json/neighborhoods.geojson','r'))
	return jsonify(neighborhoods)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8000)
