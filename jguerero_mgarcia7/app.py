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

# class app(dml.Algorithm):
# 	contributor = 'jguerero_mgarcia7'
# 	reads = ['jguerero_mgarcia7.neighborhoodstatistics']
# 	writes = []


# 	@staticmethod
# 	def execute(trial = False):
# 		'''Retrieve some data sets (not using the API here for the sake of simplicity).'''
# 		startTime = datetime.datetime.now()

# 		app_name.run(host='0.0.0.0',port=5000,debug=True)

# 		endTime = datetime.datetime.now()

# 		return {"start":startTime, "end":endTime}

# 	@staticmethod
# 	def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
# 		'''
# 			Create the provenance document describing everything happening
# 			in this script. Each run of the script will generate a new
# 			document describing that invocation event.
# 			'''

# 		# Set up the database connection.
# 		client = dml.pymongo.MongoClient()
# 		repo = client.repo
# 		repo.authenticate('jguerero_mgarcia7', 'jguerero_mgarcia7')
# 		doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
# 		doc.add_namespace('dat', 'http://datamechanics.io/data/jguerero_mgarcia7') # The data sets are in <user>#<collection> format.
# 		doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
# 		doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.

# 		this_script = doc.agent('alg:jguerero_mgarcia7#app', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
		
# 		neighborhoodstatistics_resource = doc.entity('dat:neighborhoodstatistics', {'prov:label':'Neighborhood Statistics', prov.model.PROV_TYPE:'ont:DataSet'})


# 		get_visualizations = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

# 		doc.wasAssociatedWith(get_statistics, this_script)
# 		doc.usage(get_statistics, neighborhoodstatistics_resource, startTime, None,
# 				  {prov.model.PROV_TYPE:'ont:Computation'}
# 				  )
 
# 		app = doc.entity('dat:jguerero_mgarcia7#app', {prov.model.PROV_LABEL:'Visualization', prov.model.PROV_TYPE:'ont:DataSet'})
# 		doc.wasAttributedTo(app, this_script)
# 		doc.wasGeneratedBy(app, get_visualizations, endTime)
# 		doc.wasDerivedFrom(app, neighborhoodstatistics_resource, get_visualizations, get_visualizations, get_visualizations)


# 		repo.logout()
				  
# 		return doc


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
def correlationjson(x, y):
	#return {x: , y:, name:''}

	stats = json.loads(nbstats())
	v = stats['features']
#	print (stats)
	
	if x == 'income' and y == 'obesity':
		complete = []
		for i in v:
			no = {'avg_num_food', 'dist_closest', 'quality_food'}
			temp = {} 
			dic = {key: val for key, val in i['properties'].items() if key not in no}
		#	print (dic)
			temp = {'x': 0, 'y': 0, 'name': 'empty'}
			temp['x'] = dic['avg_income']
			temp['y'] = dic['obesity']
			temp['name'] = dic['name']
			print (temp)
			complete.append(temp)



	# abc = {"type":"insecure","id":"1","name":"peter"}
	# black_list = {"type"}
	# rename ={"id":"identity"}  #use a mapping dictionary in case you want to rename multiple items
	# dic = {rename.get(key,key) : val for key ,val in abc.items() if key not in black_list}
	# print dic

	return json.dumps(complete)

#v = nbstats()
v = other('income', 'obesity')
print (v)


# if __name__ == "__main__":
# 	app_name.run(host='0.0.0.0',port=5000,debug=True)