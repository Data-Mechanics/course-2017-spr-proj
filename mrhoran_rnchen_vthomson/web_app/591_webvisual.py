import json #schema
from flask import Flask, jsonify, abort, make_response, request, render_template
#from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
#auth = HTTPBasicAuth()

@app.route('/')
@app.route('/index')

def index():
    return render_template('homepage.html',
                            title='Home')

@app.route('/schoolHubs')
def getSchoolHubs():
	'''returns json object of allschool hubs'''
	schoolHubs = json.load(open('../visualization/kmeans-visual/kmeans_hubs.json','r'))
	return jsonify(schoolHubs)

@app.route('/kmeans_cost_graph')
def kmeans_cost_graph():
    return render_template('int_graph.html')

@app.route('/kmeans_visual')
def kmeans_visual():
    schoolHubs = json.load(open('../visualization/kmeans-visual/kmeans_hubs.json','r'))

    return render_template('kmeans_visual.html', 
                           school_hubs = schoolHubs)

if __name__ == '__main__':
    app.run(debug=True)
        
        