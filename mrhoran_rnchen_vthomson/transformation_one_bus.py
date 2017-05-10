# Author: Ryan Chen
# Contributor: Megan Horan


import json
import geojson
import dml
import prov.model
import datetime
import uuid
import ast
import sodapy
import time 
import rtree
import numpy as np
from tqdm import tqdm
import shapely.geometry
from geopy.distance import vincenty


# this transformation will check how many comm gardens and food pantries there are for each area
# we want to take (zipcode, #comm gardens) (zipcode, #food pantries) --> (area, #food pantries#comm gardens)

class transformation_one_bus(dml.Algorithm):

    contributor = 'mrhoran_rnchen'

    reads = ['mrhoran_rnchen_vthomson.students']

    writes = ['mrhoran_rnchen_vthomson.student_per_school',
              'mrhoran_rnchen_vthomson.buses_per_yard',
              'mrhoran_rnchen_vthomson.average_distance_students']

    @staticmethod
    def execute(trial = True):
        
        startTime = datetime.datetime.now()

        client = dml.pymongo.MongoClient()

        repo = client.repo
        
        repo.authenticate('mrhoran_rnchen_vthomson', 'mrhoran_rnchen_vthomson')
        
        X = project([x for x in repo.mrhoran_rnchen_vthomson.students.find({})], get_students)

        X2 = project(X, lambda t: (t[0], 1))

        X3 = aggregate(X2, sum)
        
        students_per_school = project(select(product(X,X3), lambda t: t[0][0] == t[1][0]), lambda t: (t[0][0],(t[0][1], t[1][1])))

        # I just want to get the average number of students per school 
        x = project(students_per_school, lambda t: t[1][1])

        averagenum_studentsperschool = 0
        
        for i in range(len(x)):
            averagenum_studentsperschool += x[i]
            
        averagenum_studentsperschool = averagenum_studentsperschool/ (len(x))
        print("this is the average number of students per school:")
        print(averagenum_studentsperschool)
                        
        repo.dropCollection('student_per_school')
        repo.createCollection('student_per_school')

        repo.mrhoran_rnchen_vthomson.student_per_school.insert(dict(students_per_school))

        # buses needed for school
        
############################
## FIND THE AVERAGE # CASE DISTANCE BETWEEN STUDENTS ** (MAYBE WORST CASE DISTANCE)

        student_locations = [(f, shapely.geometry.shape(f['geometry'])) for f in tqdm(geojson.loads(open('input_data/students-simulated.geojson').read())['features']) if f['geometry'] is not None]

        if trial == True:
            student_locations = student_locations[:((int)(len(student_locations)/16))]

        student_data = geojson.load(open('input_data/students-simulated.geojson'))


	   #fill 3tree
        p = rtree.index.Property()
        student_tree = rtree.index.Index(properties=p)
        for i in tqdm(range(len(student_locations))):
              (f,s) = student_locations[i]
              student_tree.insert(i, s.bounds)

        
        avgs = []
        #average distance to nearest other students for each student
        student_radius = []
        
        for i in tqdm(range(len(student_locations))):

              sv = student_locations[i][0]['geometry']['coordinates']
              m = (sv[0][0],sv[0][1],sv[0][0],sv[0][1])
              near = list(student_tree.nearest(m,1,True))
              n = [x.bbox for x in near]

              d = [vincenty((m[0],m[1]),(c[0],c[1])).miles for c in n]
              d.sort()
              student_radius.append([s for s in d if s < 0.5])  #average # students in a .5 mile radius
 
              avgs.append(np.sum([d[i] for i in range(min(10,len(d)))])/10) # average distance b/w 10 closest students 
              
 
        print("Average Distance to 10 nearest students of student 0: ") 
        print(avgs[0])
        print("Distances to students within a 0.5 mile radius: ")
        print(student_radius[0])
        print("Values for each student stored in avgs and student_radius")

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}

    
    @staticmethod
    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
            '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('mrhoran_rnchen_vthomson', 'mrhoran_rnchen_vthomson')
        
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        #doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')

        this_script = doc.agent('dat:mrhoran_rnchen_vthomson#transformation_one_bus', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})

        resource1 = doc.entity('dat:_bps_transportation_challenge/students.json', {'prov:label':'Student Aggregation', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})

        get_student_per_school = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_student_per_school, this_script)

        doc.usage(get_student_per_school, resource1, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'
                  #'ont:Query':'location, area, coordinates, zip_code' #?type=Animal+Found&$select=type,latitude,longitude,OPEN_DT'
                  }
                  )

        # Used resource2 --> average_distance_students uses students.json
        get_average_distance_students = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_average_distance_students, this_script)

        doc.usage(get_average_distance_students, resource1, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'
                  #'ont:Query':'location, area, coordinates, zip_code' #?type=Animal+Found&$select=type,latitude,longitude,OPEN_DT'
                  }
                  )
    
        student_per_school = doc.entity('dat:mrhoran_rnchen_vthomson#student_per_school', {prov.model.PROV_LABEL:'Students per school', prov.model.PROV_TYPE:'ont:DataSet','ont:Extension':'json'})
        doc.wasAttributedTo(student_per_school, this_script)
        doc.wasGeneratedBy(student_per_school, get_student_per_school, endTime)
        doc.wasDerivedFrom(student_per_school, resource1, get_student_per_school, get_student_per_school, get_student_per_school)


        average_distance_students = doc.entity('dat:mrhoran_rnchen_vthomson#average_distance_students', {prov.model.PROV_LABEL:'Distance between students', prov.model.PROV_TYPE:'ont:DataSet','ont:Extension':'json'})
        doc.wasAttributedTo(average_distance_students, this_script)
        doc.wasGeneratedBy(average_distance_students, get_average_distance_students, endTime)
        doc.wasDerivedFrom(average_distance_students, resource1, get_average_distance_students, get_average_distance_students, get_average_distance_students)       

        repo.logout()
                  
        return doc

def dist(p, q):
    (x1,y1) = p
    (x2,y2) = q
    return (x1-x2)**2 + (y1-y2)**2

def aggregate(R, f):
    keys = {r[0] for r in R}
    return [(key, f([v for (k,v) in R if k == key])) for key in keys]
    
def select(R, s):
    return [t for t in R if s(t)]

def project(R, p):
    return [p(t) for t in R]

def product(R, S):
    return [(t,u) for t in R for u in S]

def find_location_students(student):

    lat = float(student["Latitude"])
    lon = float(student["Longitude"])
    school_start_time = ["Current School Start Time"]

    return((school_start_time,(lat,lon)))  

def get_students(student): # want to return the coordinates of the towns in and around Boston

    name = student["Assigned School"]
    
    if(student["Assigned School"] == "Sr. Kennedy School"):

        name = "Sr Kennedy School"
        
    return((name, (student["School Longitude"], student["School Latitude"])))


transformation_one_bus.execute()
doc = transformation_one_bus.provenance()
print(doc.get_provn())
#print(json.dumps(json.loads(doc.serialize()), indent=4))

### eof
