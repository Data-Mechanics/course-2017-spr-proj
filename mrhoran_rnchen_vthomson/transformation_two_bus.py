# Author: Megan Horan
# Contributor: Ryan Chen

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

class transformation_two_bus(dml.Algorithm):

    contributor = 'mrhoran_rnchen_vthomson'

    reads = ['mrhoran_rnchen_vthomson.schools',
            'mrhoran_rnchen_vthomson.buses']

    writes = ['mrhoran_rnchen_vthomson.kmeans_school_hubs_ideal',
             'mrhoran_rnchen_vthomson.kmeans_school_hubs_current']

    @staticmethod
    def execute(trial = False):
        
        startTime = datetime.datetime.now()

        client = dml.pymongo.MongoClient()

        repo = client.repo
        
        repo.authenticate('mrhoran_rnchen_vthomson', 'mrhoran_rnchen_vthomson')

        ## For this transformation we want to focus on using k means to look at the hubs of schools
        ## we are going to focus on the effects of different numbers of k and its effects on the means

        # transforming the data to get the latitude and longitude of the schools
        S = project([x for x in repo.mrhoran_rnchen_vthomson.schools.find({})], get_school_locations)
        
        # standard Kmeans algorithm
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

        ## this costs function will go through all the points, find the closest mean to each point, and find the distance between them
        ## it will construct an array with every point and the cost(vincety distance) to its closest mean
        ## finally it returns the average cost and the standard deviation
        
        def costs(S, M):

            # initialize return array
            cost_array = [0]*(len(S))
            closest_k = 1000
        
            for j in range(len(S)):
                closest_k = 1000
                
                # for each school go through evey mean and find the closest mean
                for i in range(len(M)):

                    distance = (vincenty(S[j], M[i]).miles)
                
                    # if you found a closer mean update the closest_k variable
                    if (distance < closest_k):
                        
                        closest_k = distance
                       
                # update the array for reflect that points cost to their local mean
                cost_array[j] = closest_k

        
            # here we calculate the standard deviation from all those costs
            standard_dev = np.std(cost_array)
                    
                
            ## find the cost by adding up all the distances and diving it by the number of distances to get the average
            ## cost value for each point.. ie how close do the means get to each point
            
            overall_cost = 0

            for i in range(len(cost_array)):

                overall_cost += cost_array[i]

            return([(overall_cost/len(cost_array)), standard_dev])

        
        ## added function to make our map nicer
        ## the closest mean array tells us which points match up to which mean: but I also want it to give a count so that
        ## when we go to graph cirles on a map, I want the size of the circle to reflect how may schools are serviced
        ## by that mean
        
        def close_mean_count(S, M):
            
            closest_mean = [0]*(len(S))
            closest_k = 1000
        
            for j in range(len(S)):
                closest_k = 1000
                
                for i in range(len(M)):

                    distance = (vincenty(S[j], M[i]).miles)
                
                    if (distance < closest_k):
                        
                        closest_k = distance
                        closest_mean[j] = M[i]

                
            return(closest_mean)

        # for testing purposes:
        
        #if trial is true then we want to do it on a small subset of the data
        
        if(trial == True):

            ## running on a dataset half the size
            num_means =22
        
            # picking the number of means from a random selection from (1/4) of the data

            M = [None]*num_means;

            for i in range(0, num_means):

                x = random.randint(0, len(S)-1)
                val = S[x]
                M[i] = val

            # cutting the data set in half
            x = int(len(S)/2)
        
            P1 = [None]*x

            for i in range(x):
            
                P1[i] = S[i]

           # find the means returned by kmeans
            mean = k_means(P1, M)
            
            # find the cost
            cost = costs(P1, mean)

            print("cost of " + str(num_means) +" is "+ str(cost[0]))
            print("stdDev of " + str(num_means) +" is "+ str(cost[1]))
            print("here are the ideal locations of the busyards")
            print(mean)
            return(mean)
           

        ## if trial is set to false, just do things normally on the whole dataset
        else:

            #after running various test, cost of more means dropped off around here
            
################## section made for csv file functionality #######################################################################
            csv_row_cost = [None]*87
            csv_row_std =  [None]*87
            
            # this outer for loop will go through and test k-values in range 0-87 (the length of the schools dataset)
            
            for i in range(1, 87):

                num_means = i

                # picking the number of means from a random selection of the data

                M = [None]*num_means
                
                for i in range(0, num_means):

                    x = random.randint(0, len(S)-1)
                    val = S[x]
                    M[i] = val

                # find the means for that k-value
                mean = k_means(S, M)
               
                # we want to save the means at the ideal k-value of 44
                if(i == 44):
                    
                    mean_ideal = mean
                    
                # now we find the average cost and standard deviation between all the points in the dataset, S ,and the means found above
            
                cost_combined = (costs(S, mean))
                
                # we want to update these arrays because will be outputed to a csv file for graph use
                csv_row_cost[i] = cost_combined[0]
                csv_row_std[i] = cost_combined[1]

            # writing to the csv file
#
            with open("/Users/meganhoran/Desktop/cs591/kmeans_stats.csv", "w") as csv_file:

                writer = csv.writer(csv_file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

                for i in range(86):

                    writer.writerow([csv_row_cost[i], csv_row_std[i], i])
                    
###################################################################################################################################

            # now we want to insert the ideal number of means and their locations into mongod 
            # we know that the ideal number of means is roughly half the dataset, as seen from the graph produced from the csv

            closest_mean = close_mean_count(S, mean_ideal)

            closest_mean_2 = project(closest_mean, lambda t: ((t[0] ,t[1]), 1))
            
            closest_mean_3 = aggregate(closest_mean_2, sum)

            # formating to put in the database
            for i in range(len(closest_mean_3)):
                str_ = "bus_yard" + str(i)
                closest_mean_3[i] = (str_, ((closest_mean_3[i][0][0],  closest_mean_3[i][0][1]), closest_mean_3[i][1]))

            
            repo.dropCollection('mrhoran_rnchen_vthomson.kmeans_school_hubs_ideal')
            repo.createCollection('mrhoran_rnchen_vthomson.kmeans_school_hubs_ideal')

            repo.mrhoran_rnchen_vthomson.kmeans_school_hubs.insert(dict(closest_mean_3))

################# finally we want to insert the current number of means and their locations into mongod ###########################
            
            ## finding the current school locations
            Y = project([p for p in repo.mrhoran_rnchen_vthomson.buses.find({})], get_buses)

            Y2 = project(Y, lambda t: (t[1], 1))

            Y3 = aggregate(Y2, sum)
            
            current_schools_locations = [None]*len(Y3)
            
            for i in range(len(Y3)):
                current_schools_locations[i] = Y3[i][0]
                
            # now we want to find the closest schools to all those means and put them in a database!
            current_closest_mean = close_mean_count(S, current_schools_locations)
            current_closest_mean_2 = project(current_closest_mean, lambda t: ((t[0] ,t[1]), 1))
            current_closest_mean_3 = aggregate(current_closest_mean_2, sum)
            
            
            for i in range(len(current_closest_mean_3)):
                str_ = "current_yard" + str(i)
                current_closest_mean_3[i] = (str_, ((current_closest_mean_3[i][0][0],  current_closest_mean_3[i][0][1]), current_closest_mean_3[i][1]))
                
            repo.dropCollection('mrhoran_rnchen_vthomson.kmeans_school_hubs_current')
            repo.createCollection('mrhoran_rnchen_vthomson.kmeans_school_hubs_current')

            repo.mrhoran_rnchen_vthomson.buses_per_yard.insert(dict(current_closest_mean_3))

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
        
        resource1 = doc.entity('dat:schools', {'prov:label':'Ideal Busyards', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})

        get_kmeans_schools = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_kmeans_schools, this_script)

        doc.usage(get_kmeans_schools, resource1, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'
                  }
                  )
        kmeans = doc.entity('dat:mrhoran_rnchen#kmeans_school_hubs_ideal', {prov.model.PROV_LABEL:'Ideal Busyards', prov.model.PROV_TYPE:'ont:DataSet','ont:Extension':'json'})
        doc.wasAttributedTo(kmeans, this_script)
        doc.wasGeneratedBy(kmeans, get_kmeans_schools, endTime)
        doc.wasDerivedFrom(kmeans, resource1, get_kmeans_schools, get_kmeans_schools, get_kmeans_schools)
        repo.logout()
                  
        resource2 = doc.entity('dat:buses', {'prov:label':'bus yards', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})

        get_current_schools = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_current_schools, this_script)

        doc.usage(get_current_schools, resource2, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'
                  }
                  )
        kmeans2 = doc.entity('dat:mrhoran_rnchen#kmeans_school_hubs_current', {prov.model.PROV_LABEL:'Current Busyards', prov.model.PROV_TYPE:'ont:DataSet','ont:Extension':'json'})
        doc.wasAttributedTo(kmeans2, this_script)
        doc.wasGeneratedBy(kmeans2, get_current_schools, endTime)
        doc.wasDerivedFrom(kmeans2, resource2, get_current_schools, get_current_schools, get_current_schools)
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
        
def get_buses(bus): # want to return the coordinates of bus yards and their name

    lat = bus['Bus Yard Latitude']
    lon = bus['Bus Yard Longitude']

    name = bus['Bus Yard']

    return((name,(lat,lon)))


transformation_two_bus.execute()
doc = transformation_two_bus.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof
