# Project #2
# This class is used to get nearby transit stops within a 1km radius for a given residential property. 
# We get the transit stations from queries to the Google Places Web Services API
#
# This data will be used for our constraint satisfaction optimization problem

import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import z3
from math import radians, cos, sin, asin, sqrt
import sys
import random

class res_transit_pull(dml.Algorithm):
	contributor = 'mbyim_seanz'
	reads = ['mbyim_seanz.property_assessments']
	writes = ['mbyim_seanz.residential_transit']

	@staticmethod
	def execute(trial = False):
		startTime = datetime.datetime.now()

		client = dml.pymongo.MongoClient()
		repo = client.repo

		# Connect to mongoDB
		repo.authenticate('mbyim_seanz', 'mbyim_seanz')

		#get property assessments----------------
		property_assessments_data = repo.mbyim_seanz.property_assessments.find()

		# get residential property latitude and longitude, used as an intermediate piece of data
		# Dictionary of the form:
		# { point #: [latitude, longitude, property cost, res_address, res_zipcode] }
		final_residential_property = {}
		point_counter = 0
		for row in property_assessments_data:
			dict_property = dict(row)
			if 'R' in dict_property["lu"] or dict_property["lu"] == 'CD':
				# lat and long come in a location tuple, but as a string:
				# i.e. "(42.340297000, -71.166757000)"
				# so we need to parse:
				lat = float(dict_property["location"].split(',')[0][1:])
				lng = float(dict_property["location"].split(',')[1][:-1])
				total = dict_property["av_total"]
				parcel_id = dict_property["parcel_id"]
				res_address = dict_property["full_address"]
				res_zipcode = dict_property["zipcode"]

				final_residential_property[point_counter] = [lat,lng,total,parcel_id,res_address,res_zipcode]
				point_counter += 1

		# print('got residential property')

		final_data_set = []
		count = 0

		google_places_key = dml.auth['services']['googleplacesapi']['key']

		original_stdout = sys.stdout
		# sys.stdout = open('res_transit.txt', 'w')

		randomized_res_keys = list(final_residential_property.keys())
		random.shuffle(randomized_res_keys)

		# finding shortest transit stop within a 1 km radius to every given residential property
		# The data will be stored of the form
		#	{ 
		# 		"parcel_id" : parcel_id,
		#		"res_transit_data" :
		#			{
		#				"res_address": res_address,
		#				"res_zipcode": res_zipcode,
		#				"res_lat": res_lat,
		#				"res_lng": res_lng,
		#				"cost": cost,
		#				"nearby_stops" : [
		#					{
		#						"stop_name": stop_name,
		#						"stop_lat": stop_lat,
		#						"stop_lng": stop_lng
		#					},
		#					...
		#					{
		#						"stop_name": stop_name,
		#						"stop_lat": stop_lat,
		#						"stop_lng": stop_lng
		#					},
		#				]
		#			}
		#	}
		# print('finding some google maps stuff')

		print('getting residential transit data from google maps API...')

		for residential_property in randomized_res_keys:
			# there are 133,000 residential properties, but we cannot query the Google Map API this many times in a feasible time 
			# frame, so we limited it to 2,000 residential properties
			if count > 2000:
				break

			# if trial flag is on, then only query 50
			if trial == True and count > 50:
				break
				
			res_transit_dict = {} #final dictionary
			sub_dict = {} 			#sub dictionary for res_transit_data
			res_lat = final_residential_property[residential_property][0]
			res_lng = final_residential_property[residential_property][1]
			cost = final_residential_property[residential_property][2]
			parcel_id = final_residential_property[residential_property][3]
			res_address = final_residential_property[residential_property][4]
			res_zipcode = final_residential_property[residential_property][5]

			sub_dict["res_address"] = res_address
			sub_dict["res_lat"] = res_lat
			sub_dict["res_lng"] = res_lng
			sub_dict["cost"] = cost
			sub_dict["res_zipcode"] = res_zipcode

			google_places_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(res_lat) + ',' + str(res_lng) + '&radius=1000&type=transit_station&key=' + google_places_key

			try:
				response = urllib.request.urlopen(google_places_url).read().decode("utf-8")
			except urllib.error.HTTPError as e:
				print(e.read())
				pass
			transit_stations = json.loads(response)
			transit_stations = transit_stations['results']

			nearby_stops_list = []
			for i in range(len(transit_stations)):
				single_stop_dict = {}
				stop_name = transit_stations[i]['name']
				stop_location = transit_stations[i]['geometry']['location']
				stop_lat = stop_location['lat']
				stop_lng = stop_location['lng']

				single_stop_dict["stop_name"] = stop_name
				single_stop_dict["stop_lat"] = stop_lat
				single_stop_dict["stop_lng"] = stop_lng

				nearby_stops_list.append(single_stop_dict)
			sub_dict["nearby_stops"] = nearby_stops_list
			res_transit_dict["parcel_id"] = parcel_id
			res_transit_dict["res_transit_data"] = sub_dict

			# print(json.dumps(res_transit_dict), end=",") out to a text file

			final_data_set.append(res_transit_dict)
			count += 1
		
		# sys.stdout.close()
		# sys.stdout = original_stdout
		final_data_string_fixed = json.dumps(final_data_set)
		final_data_string_fixed.replace("'", '"')
		# print('done')
		
		r = json.loads(final_data_string_fixed)
		s = json.dumps(r, sort_keys=True, indent=2)

		repo.dropCollection("residential_transit")
		repo.createCollection("residential_transit")
		repo['mbyim_seanz.residential_transit'].insert_many(r)
		repo['mbyim_seanz.residential_transit'].metadata({'complete':True})
		print('got residential transit data from google maps')
		print(repo['mbyim_seanz.residential_transit'].metadata())
	
	@staticmethod
	def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
		client = dml.pymongo.MongoClient()
		repo = client.repo
		repo.authenticate('mbyim_seanz', 'mbyim_seanz')

		doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
		doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
		doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
		doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
		doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')
		doc.add_namespace('mbta', 'http://realtime.mbta.com/developer/api/v2/stopsbyroute')
		doc.add_namespace('gmaps', 'https://maps.googleapis.com/maps/api/place/nearbysearch/json')

		this_script = doc.agent('alg:mbyim_seanz#res_transit_pull', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
		resource_res_transit = doc.entity('gmaps:type=transit_station', {'prov:label':'Residential Transit Stations', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
		get_res_transit = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

		doc.wasAssociatedWith(get_res_transit, this_script)

		doc.usage(get_res_transit, resource_res_transit, startTime, None,
		          {prov.model.PROV_TYPE:'ont:Retrieval',
		          'ont:Query':'?location=lat,lng&radius=1000&type=transit_station&key=api_key' 
		          }
		)

		res_transit = doc.entity('dat:mbyim_seanz#res_transit', {prov.model.PROV_LABEL:'Residential Transit Stations', prov.model.PROV_TYPE:'ont:DataSet'})
		doc.wasAttributedTo(res_transit, this_script)
		doc.wasGeneratedBy(res_transit, get_res_transit, endTime)
		doc.wasDerivedFrom(res_transit, resource_res_transit, get_res_transit, get_res_transit, get_res_transit)

		repo.logout()
		          
		return doc


# res_transit_pull.execute()
# doc = res_transit_pull.provenance()
# print('finished res transit pull')