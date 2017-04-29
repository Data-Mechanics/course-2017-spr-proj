import dml

from flask import Flask
from flask import render_template

import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")


@app.route("/nbjson")
def nbstats():
	client = dml.pymongo.MongoClient()
	repo = client.repo
	repo.authenticate('jguerero_mgarcia7', 'jguerero_mgarcia7')

	# Get stats for neighborhoods
	FIELDS = {'_id': False, 'Average Obesity (%)':True, "FoodScore":True, "Average Income ($)":True, "Neighborhood":True, "dist_closest": True, "avg_num_food": True, "quality_food":True}
	stats = {n['Neighborhood']:n for n in repo['jguerero_mgarcia7.neighborhoodstatistics'].find(projection=FIELDS)}


	FIELDS = {'name': True, 'the_geom': True, '_id': False}
	neighborhoods = []
	idx = 0
	for n in repo['jguerero_mgarcia7.neighborhoods'].find(projection=FIELDS):
		try:
			pnb = stats[n["name"]]
			neighborhoods.append({"type":"Feature", "id":idx, 
								"properties": {"name":n["name"], "obesity": pnb['Average Obesity (%)'], 
								"score": pnb["FoodScore"], "avg_income": pnb["Average Income ($)"], 
								"dist_closest": pnb["dist_closest"], "avg_num_food":pnb["avg_num_food"], 
								"quality_food":pnb["quality_food"] }, 
								"geometry":n['the_geom']})

			idx += 1
		except KeyError:
			continue


	tot = {"type":"FeatureCollection", "features": neighborhoods}

	gj = json.dumps(tot, default=json_util.default)

	repo.logout()
	return gj



if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000,debug=True)