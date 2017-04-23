import urllib.request
import json
import dml
import datetime
import uuid
import requests
import numpy as np
import math
import prov.model

# visual1 data function
class VisualOne(dml.Algorithm):
	contributor = 'asafer_asambors_maxzm_vivyee'
	reads = ['asafer_asambors_maxzm_vivyee.obesity_time']
	writes = []

	@staticmethod
	def execute():
		return get_data(0, 100000)

	@staticmethod
	def provenance():
		pass

	@staticmethod
	def get_data(min_pop, max_pop):
		# for now, ignore pop until the graph is working. Then use pop to filter here

		# set up the connection
		client = dml.pymongo.MongoClient()
		repo = client.repo
		repo.authenticate('asafer_asambors_maxzm_vivyee', 'asafer_asambors_maxzm_vivyee')

		# loads
		obesity_time = repo['asafer_asambors_maxzm_vivyee.obesity_time'].find()
		obesity_time_tuples = [[a['time'], a['data_value']] for a in obesity_time]

		# X that will be returned (time to get to healthy location)
		X = np.array(obesity_time_tuples)[:,0]
		# Y that will be returned (obesity percentage)
		Y = np.array(obesity_time_tuples)[:,1] 

		# linear regression code
		meanX = sum(X)*1.0/len(X)
		meanY = sum(Y)*1.0/len(Y)

		varX = sum([(v-meanX)**2 for v in X])
		varY = sum([(v-meanY)**2 for v in Y])

		minYHatCov = sum([(X[i]-meanX)*(Y[i]-meanY) for i in range(len(Y))])

		B1 = minYHatCov/varX
		B0 = meanY - B1*meanX

		yhat = []
		for i in range(len(X)):
			yhat += [B0 + (X[i]*B1)]

		data = []
		for i in range(len(Y)):
			data += [{"yhat": yhat[i],
					"y": Y[i],
					"x": X[i]}]

		return data
