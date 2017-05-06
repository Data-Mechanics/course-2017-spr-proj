# some kmeans shenanigans

import json
import dml
import prov.model
import datetime
import uuid
import ast
import random
import sodapy
from geopy.distance import vincenty
import time
import numpy as np
import csv

# this transformation will check how many comm gardens and food pantries there are for each area
# we want to take (zipcode, #comm gardens) (zipcode, #food pantries) --> (area, #food pantries#comm gardens)
# I think this is a selection and aggregation

class transformation_two_bus(dml.Algorithm):

    contributor = 'mrhoran_rnchen_vthomson'

    reads = ['mrhoran_rnchen_vthomson.schools']

    writes = ['mrhoran_rnchen_vthomson.kmeans_school_hubs']


    @staticmethod
    def execute(trial = False):
        
        startTime = datetime.datetime.now()

        client = dml.pymongo.MongoClient()

        repo = client.repo
        
        repo.authenticate('mrhoran_rnchen_vthomson', 'mrhoran_rnchen_vthomson')

        ## For this transformation we want to focus on using k means to look at the hubs of schools
        ## we are going to focus on the effects of different numbers of k and its effects on the means


        ## getting coordinates of sc
        S = project([x for x in repo.mrhoran_rnchen_vthomson.schools.find({})], get_school_locations)
        #print(S)

        
        def k_means(P,M):
            
            OLD = []
        
            while OLD != M:
                
                OLD = M

                MPD = [(m, p, dist(m,p)) for (m, p) in product(M, P)]
                PDs = [(p, dist(m,p)) for (m, p, d) in MPD]
                PD = aggregate(PDs, min)
                MP = [(m, p) for ((m,p,d), (p2,d2)) in product(MPD, PD) if p==p2 and d==d2]
                MT = aggregate(MP, plus)

                M1 = [(m, 1) for ((m,p,d), (p2,d2)) in product(MPD, PD) if p==p2 and d==d2]
                MC = aggregate(M1, sum)

                M = [scale(t,c) for ((m,t),(m2,c)) in product(MT, MC) if m == m2]
                
                return(sorted(M))

        ## calculating the cost now

        ## first we want to go through and see which mean is the closest, and keep that distance
        ## store that in a big array

        def costs(S, M):

            cost_array = [0]*(len(S))
            closest_k = 1000

            #print(vincenty(newport_ri, cleveland_oh).miles)
        
            for j in range(len(S)):
                closest_k = 1000
                for i in range(len(M)):

                    distance = (vincenty(S[j], M[i]).miles)
                
                    if (distance < closest_k):
                        
                        closest_k = distance
                        
                cost_array[j] = closest_k

            # to find standard deviation for a graph
           # for j in range(len(cost_array)):

            standard_dev = np.std(cost_array)
            #print(standard_dev)
                    
                
            ## find the cost by adding up all the distances and diving it by the number of distances to get the average
            ## cost value for each point.. ie how close do the means get and is there a drop off in terms of productivity
           
            overall_cost = 0

            for i in range(len(cost_array)):

                overall_cost += cost_array[i]

            return([(overall_cost/len(cost_array)), standard_dev])

        ## added function to make our map nicer
        
        ## the closest mean array tells us which points match up to which mean: I want it to give a count so that
        ## when we go to graph cirles on a map, I want the size of the circle to reflect how may schools are serviced
        ## by that mean
        
        def close_mean_count(S, M):
            
            closest_mean = [0]*(len(S))
            
            closest_k = 1000

            #print(vincenty(newport_ri, cleveland_oh).miles)
        
            for j in range(len(S)):
                closest_k = 1000
                for i in range(len(M)):

                    distance = (vincenty(S[j], M[i]).miles)
                
                    if (distance < closest_k):
                        
                        closest_k = distance
                        closest_mean[j] = M[i]

                
            return(closest_mean)


        # if trial is true then we want to do it on a small subset of the data
        
        if(trial == True):

            ## running on a dataset half the size
            num_means =22
        

            # picking the number of means from a random selection from (1/4) of the data

            M = [None]*num_means;

            for i in range(0, num_means):

                x = random.randint(0, len(S)-1)
                val = S[x]
                M[i] = val

            x = int(len(S)/2)
        
            P1 = [None]*x

            for i in range(x):
            
                P1[i] = S[i]

            mean = k_means(P1, M)
            
            cost = costs(P1, mean)

            print("cost of " + str(num_means) +" is "+ str(cost))
            print("here are the new means")
            print(mean)
            return(mean)
           

        ## otherwise just do things normally
        else:

            #after running various test, cost of more means dropped off around here
            csv_row_cost = [None]*87
            csv_row_std =  [None]*87
            
            for i in range(1, 87):

                num_means = i

                # picking the number of means from a random selection of the data

                M = [None]*num_means
                

                for i in range(0, num_means):

                    x = random.randint(0, len(S)-1)
                    val = S[x]
                    M[i] = val

                
                mean = k_means(S, M)
               

                # now we find the average cost and standard deviation between all the points in the dataset, S ,and the its means
            
                cost_combined = (costs(S, mean))
                # we want to update these arrays because will be outputed to a csv file for graph use
                csv_row_cost[i] = cost_combined[0]
                csv_row_std[i] = cost_combined[1]

            # writing to the csv file

            with open("/Users/meganhoran/Desktop/cs591/kmeans_stats.csv", "w") as csv_file:

                writer = csv.writer(csv_file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

                for i in range(86):

                    writer.writerow([csv_row_cost[i], csv_row_std[i], i])

            # fianlly, we want to insert the means into a dictionanry

            closest_mean = close_mean_count(S, mean)

            closest_mean_2 = project(closest_mean, lambda t: ((t[0] ,t[1]), 1))
            
            closest_mean_3 = aggregate(closest_mean_2, sum)

            # formating to put in the database
            for i in range(len(closest_mean_3)):
                str_ = "bus_yard" + str(i)
                closest_mean_3[i] = (str_, ((closest_mean_3[i][0][0],  closest_mean_3[i][0][1]), closest_mean_3[i][1]))

            print("******")
            print(closest_mean_3)
            repo.dropCollection('mrhoran_rnchen_vthomson.kmeans_school_hubs')
            repo.createCollection('mrhoran_rnchen_vthomson.kmeans_school_hubs')

            repo.mrhoran_rnchen_vthomson.kmeans_school_hubs.insert(dict(closest_mean_3))

           # now we want to find how many schools there are for each mean
           
            repo.logout()

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
        doc.add_namespace('dat', 'http://datamechanics.io/?prefix=_bps_transportation_challenge/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
##
        this_script = doc.agent('alg:mrhoran_rnchen_vthomson#transformation_two_bus', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        
        resource1 = doc.entity('dat:schools', {'prov:label':'Kmeans Schools', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})

        get_kmeans_schools = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_kmeans_schools, this_script)

        doc.usage(get_kmeans_schools, resource1, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'
                  }
                  )
        kmeans = doc.entity('dat:mrhoran_rnchen#kmeans', {prov.model.PROV_LABEL:'Kmeans Schools', prov.model.PROV_TYPE:'ont:DataSet','ont:Extension':'json'})
        doc.wasAttributedTo(kmeans, this_script)
        doc.wasGeneratedBy(kmeans, get_kmeans_schools, endTime)
        doc.wasDerivedFrom(kmeans, resource1, get_kmeans_schools, get_kmeans_schools, get_kmeans_schools)
        repo.logout()
                  
        return doc
        return ""
def dist(p, q):
    (x1,y1) = p
    (x2,y2) = q
    return (x1-x2)**2 + (y1-y2)**2

def plus(args):
    p = [0,0]
    for (x,y) in args:
        p[0] += x
        p[1] += y
    return tuple(p)
def scale(p, c):
    (x,y) = p
    return (x/c, y/c)

def project(R, p):
    return [p(t) for t in R]

def select(R, s):
    return [t for t in R if s(t)]
def product(R, S):
    return [(t,u) for t in R for u in S]
def aggregate(R, f):
    keys = {r[0] for r in R}
    return [(key, f([v for (k,v) in R if k == key])) for key in keys]


def get_school_locations(schools):

    lat = float(schools["Latitude"])
    lon = float(schools["Longitude"])
    #name = schools["School Name"]

    x = (schools["Address"].split(','))
    
    return((lat,lon))
        
##def get_busyard_locations(bus):
##
##    lat = bus['Bus Yard Latitude']
##    long = bus['Bus Yard Longitude']
##    name =  bus['Bus Yard']
##
##    return((name, (lat,long)))
    
transformation_two_bus.execute()
doc = transformation_two_bus.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof