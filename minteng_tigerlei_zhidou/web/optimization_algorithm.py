import json
# import dml
import pymongo
import datetime
import os, json

def get_result(f,t,s,r):
	client = pymongo.MongoClient()
	repo = client.repo
	repo.authenticate('minteng_tigerlei_zhidou', 'minteng_tigerlei_zhidou')

	# user will set the grade they want
	transport=t
	food=f	
	safety=s
	rent=r

	#find the fitted area
	def if_fitted(A,requirement):#[t,f,s,r] is the requirment/standred
		[t1,f1,s1,r1]=A
		[t,f,s,r]=requirement
		if r1=='Not found':
			return False
		if t1>=t and f1>=f and s1>=s and r1>=r:
			return True
		return False
	def get_dist(A,requirement):
		[t1,f1,s1,r1]=A
		[t,f,s,r]=requirement
		if r1=='Not found':
			return 1000
		return ((t1-t)**2+(f1-f)**2+(s1-s)**2+(r1-r)**2)**0.5

	res=[]    
	a=repo['minteng_tigerlei_zhidou.box_count'].find()
	for i in a:
		grade1=[i['grade']['transport'],i['grade']['food'],i['grade']['safety'],i['grade']['rent']]
		if if_fitted(grade1,[transport,food,safety,rent]):
			temp=i
			temp['rating']=sum(i['grade'].values())
			res.append(temp)
		else:
			temp=i
			temp['rating']=get_dist(grade1,[transport,food,safety,rent])*-1
			res.append(temp)


	#return top fitted
	result=sorted(res, key=lambda x: x['rating'], reverse=True)
	top5 = result[0:5]

	for i in range(5):
		top5[i]['rank'] = i

	# get crime num
	crimeCount=[]
	b=repo['minteng_tigerlei_zhidou.crimeCount'].find()
	for i in b:
		for j in top5:
			if (j['box'] == i['box']):
				temp = {}
				temp['crimeNum'] = i['crimeNum']
				temp['rank'] = j['rank']
				crimeCount.append(temp)

	current_dir = os.getcwd()

	# Create datadir if does not exist
	if not os.path.exists(os.path.join(current_dir, 'top5.json')):
		with open('top5.json', 'w') as f:
			json.dump(crimeCount,f)

	# for mapping
	for i in result:
		i['center']=[(i['box'][0][0]+i['box'][1][0])/2,(i['box'][0][1]+i['box'][1][1])/2]

	for i in result:
		i['leftdown']=[i['box'][0][0],i['box'][0][1]]
		i['leftup']=[i['box'][0][0],i['box'][1][1]]
		i['rightdown']=[i['box'][1][0],i['box'][0][1]]
		i['rightup']=[i['box'][1][0],i['box'][1][1]]

	return result

#print(get_result(3,4,3,4)[0])
