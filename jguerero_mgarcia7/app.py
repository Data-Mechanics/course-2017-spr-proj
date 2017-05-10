import dml
import prov.model
import datetime
import uuid

from flask import Flask
from flask import render_template

import json
from bson import json_util
from bson.json_util import dumps

app_name = Flask(__name__)

@app_name.route("/")
def index():
	return render_template("page.html")


@app_name.route("/nbjson")
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

@app_name.route("/correlationjson")
def correlationjson():
	#return {x: , y:, name:''}

	stats = json.loads(nbstats())
	v = stats['features']
#	print (stats)
	
	#if x == 'income' and y == 'obesity':
	complete = []
	for i in v:
		no = {'avg_num_food', 'dist_closest', 'quality_food'}
		temp = {} 
		dic = {key: val for key, val in i['properties'].items() if key not in no}
	#	print (dic)
		temp = {'x': 0, 'y': 0, 'name': 'empty'}
		temp['x'] = dic['score']
		temp['y'] = dic['obesity']
		temp['name'] = dic['name']
		complete.append(temp)



	# abc = {"type":"insecure","id":"1","name":"peter"}
	# black_list = {"type"}
	# rename ={"id":"identity"}  #use a mapping dictionary in case you want to rename multiple items
	# dic = {rename.get(key,key) : val for key ,val in abc.items() if key not in black_list}
	# print dic
	print (complete)
	return complete

#v = nbstats()
#v = correlationjson('income', 'obesity')
# print (v)


if __name__ == "__main__":
	app_name.run(host='0.0.0.0',port=5000,debug=True)