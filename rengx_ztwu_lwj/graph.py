#!/usr/bin/python

import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import ssl
from pymongo import MongoClient
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt


class graph(dml.Algorithm):
	contributor = 'rengx_ztwu_lwj'
	reads = ["rengx_ztwu_lwj.publicschool_accessibility"]
	writes = []
	
	@staticmethod
	def graph1(pad):
		#print(pad[0])
		xs = []
		ys = []
		ss = []
		for item in pad:
			xs.append(item['x'])
			ys.append(item['y'])
			ss.append(item['access_score'])
		xs = [int(n)/(1.0*1000000) for n in xs]
		ys = [0 - int(n)/(1.0*1000000) for n in ys]

		sx = 42.21275
		fx = 42.40748
		dx = fx - sx
		sy = -71.1835
		fy = -70.96343
		dy = fy - sy
		xs = [abs(n - sx)/(1.0*dx) for n in xs]
		ys = [abs(n- sy)/(1.0* dy) for n in ys]
		fig, ax = plt.subplots(figsize=(5, 6))
		img =  plt.imread('bg.png')
		ax.imshow(img, extent=[0, 1, 0, 1.2])
		colors = "bgrcmy"
		color_index = 0
		for i in range(len(xs)):
			c = plt.Circle((ys[i], xs[i]), ss[i] * 0.001, color = colors[color_index], alpha = 0.3)
			color_index = (color_index + 1) % len(colors)
			ax.add_artist(c)
		
		#plt.axis(sy, fy, sx, fx)
		plt.axis('off')
		plt.title('Graph of Boston Public School Accessibility')
		#plt.show()
		fig.savefig('BPSA.png')

	@staticmethod
	def graph2(pad):	
		xs = [x['x'] for x in pad]
		ys = [x['y'] for x in pad]
		ss = [x['access_score'] for x in pad]
		cid = [x['cid'] for x in pad]
		
		xs = [int(n)/(1.0*1000000) for n in xs]
		ys = [0 - int(n)/(1.0*1000000) for n in ys]
		sx = 42.21275
		fx = 42.40748
		dx = fx - sx
		sy = -71.1835
		fy = -70.96343
		dy = fy - sy
		xs = [abs(n - sx)/(1.0*dx) for n in xs]
		ys = [abs(n- sy)/(1.0* dy) for n in ys]
		plt.figure(2)
		fig, ax = plt.subplots(figsize=(5, 6))
		
		img =  plt.imread('bg2.png')
		ax.imshow(img, extent=[0, 1, 0, 1.2])
		colors = "bcgrm"
		for i in range(len(xs)):
			plt.plot([ys[i]],[xs[i]], colors[int(cid[i])] + '*', ms = 8)

		plt.axis('off')
		plt.title('Graph of Public School K-Means Clustering')
		#plt.show()
		fig.savefig('GPSKC.png')
	@staticmethod
	def graph3(pad):
		data = [(x['dist_central'], x['access_score']) for x in pad]
		plt.figure(3)
		fig, ax = plt.subplots()
		data.sort(key = lambda x: x[0])
		ds = [x[0] for x in data]
		ss = [x[1] for x in data]
		plt.plot(ds, ss,)
		plt.title('Correlation of Accessibility Score and Distance to Region Central')
		plt.xlabel("Distance(KM)")
		plt.ylabel("Accessibility Score")
		#plt.show()
		fig.savefig('COR.png')
			
	@staticmethod
	def execute(trial = False):
		startTime = datetime.datetime.now()
		client = dml.pymongo.MongoClient()
		repo = client.repo
		repo.authenticate("rengx_ztwu_lwj", "rengx_ztwu_lwj")
		pa = repo.publicschool_accessibility
		pa_find = pa.find()
		pad = []
		for i in pa_find:
				 pad.append(i)
		graph.graph1(pad)
		graph.graph2(pad)
		graph.graph3(pad)
		#repo.metadata.insert_one(dt)
		repo.logout()
		endTime = datetime.datetime.now()
		#print("geo complete")
		return {"start":startTime, "end":endTime}
		 
	@staticmethod
	def provenance(doc=prov.model.ProvDocument(), startTime=None, endTime=None):
		repo.logout()
		return doc														
					
graph.execute()
#doc = geo.provenance()
#print(doc.get_provn())
#print(json.dumps(json.loads(doc.serialize()), indent=4))
