import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import csv
import json
import requests
from matplotlib import pyplot as plt
import matplotlib as mp
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import sklearn.manifold
from scipy import cluster
import seaborn as sns
import sklearn.datasets as sk_data
import sklearn.metrics as metrics
from scipy.cluster.vq import kmeans2
import urllib
import time

class optimalEMSStations(dml.Algorithm):
    contributor = 'cfortuna_houset_karamy_snjan19'
    reads = ['cfortuna_houset_karamy_snjan19.CarCrashData','cfortuna_houset_karamy_snjan19.EMSStationsData']
    writes = ['cfortuna_houset_karamy_snjan19.OptimalEMSStations']

    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('cfortuna_houset_karamy_snjan19', 'cfortuna_houset_karamy_snjan19')

        # Trial Mode is basically limiting data points on which to run execution if trial parameter set to true
        #Retrieve Data
        accidents = repo['cfortuna_houset_karamy_snjan19.CarCrashData'].find()#.limit(5) if trial else repo['cfortuna_houset_karamy_snjan19.CarCrashData'].find()
        ems = repo['cfortuna_houset_karamy_snjan19.EMSStationsData'].find()

        # Creating a New repo to store the data in
        repo.dropCollection("OptimalEMSStations")
        repo.createCollection("OptimalEMSStations")

        df = pd.DataFrame(list(ems))

        df.set_index('Name', inplace=True)

        # reading the hospital locations into a pandas dataframe  
        # adjusting to proper format of x and y coordinate data

        df['Longitude'] = df['Longitude'].apply(lambda x: float(x)*1)
        df['Latitude'] = df['Latitude'].apply(lambda x: float(x)*1)

        df['long_lat'] = list(zip(df.Longitude, df.Latitude))

        # reading the crash locations into a pandas dataframe

        if trial == True:
            data = df.as_matrix([#'Station Name',
                         'Address',
                         'City',
                         'Latitude',
                         'Longitude'])
            size = len(data)
            cutoff = round(size*0.1)
            trial_data = data[:cutoff]
            df = pd.DataFrame(trial_data, columns=[#'Station Name',
                         'Address',
                         'City',
                         'Latitude',
                         'Longitude'])

        df2 = pd.DataFrame(list(accidents))

        # getting rid of null values in the the crash data

        df2.loc[pd.isnull(df2['X Coordinate']), 'Latitude'] = None
        df2.loc[pd.isnull(df2['Y Coordinate']), 'Longitude'] = None
        df2['long_lat'] = list(zip(df2['Longitude'], df2['Latitude']))

        if trial == True:
            data = df2.as_matrix(['Ambient Light',
                                  'At Roadway Intersection',
                                  'City',
                                  'Crash Date',
                                  'Crash Number',
                                  'Crash Severity',
                                  'Crash Time',
                                  'Distance from Nearest Exit',
                                  'Distance from Nearest Landmark',
                                  'Distance from Nearest Milemarker',
                                  'Distance from Nearest Roadway Intersection',
                                  'Latitude',
                                  'Longitude',
                                  'Manner of Collision',
                                  'Most Harmful Events',
                                  'Non Motorist Type',
                                  'Number of Vehicles',
                                  'Road Surface Condition',
                                  'Total Fatal Injuries',
                                  'Total Nonfatal Injuries',
                                  'Vehicle Action Prior to Crash',
                                  'Vehicle Configuration',
                                  'Vehicle Travel Directions',
                                  'Weather Condition',
                                  'X Coordinate',
                                  'Y Coordinate',
                                  'long_lat'])
            size = len(data)
            cutoff = round(size*0.1)
            trial_data = data[:cutoff]
            df2 = pd.DataFrame(trial_data, columns=['Ambient Light',
                                                   'At Roadway Intersection',
                                                   'City',
                                                   'Crash Date',
                                                   'Crash Number',
                                                   'Crash Severity',
                                                   'Crash Time',
                                                   'Distance from Nearest Exit',
                                                   'Distance from Nearest Landmark',
                                                   'Distance from Nearest Milemarker',
                                                   'Distance from Nearest Roadway Intersection',
                                                   'Latitude',
                                                   'Longitude',
                                                   'Manner of Collision',
                                                   'Most Harmful Events',
                                                   'Non Motorist Type',
                                                   'Number of Vehicles',
                                                   'Road Surface Condition',
                                                   'Total Fatal Injuries',
                                                   'Total Nonfatal Injuries',
                                                   'Vehicle Action Prior to Crash',
                                                   'Vehicle Configuration',
                                                   'Vehicle Travel Directions',
                                                   'Weather Condition',
                                                   'X Coordinate',
                                                   'Y Coordinate',
                                                   'long_lat'])

        latLongAccidents = df2.long_lat.tolist()
        latLongEMS = df.long_lat.tolist()

        cleanedAccidents = [x for x in latLongAccidents if str(x[0]) != 'nan']
        cleanedEMS = [x for x in latLongEMS if str(x[0]) != 'nan']

        emsLocations = np.asarray(cleanedEMS)
        crashLocations = np.asarray(cleanedAccidents)

        centroids, labels = kmeans2(crashLocations, k=emsLocations, iter=100, minit='matrix')

        x = []
        y = []
        for centroid in centroids:
            x.append(centroid[0])
            y.append(centroid[1])

        def stringCoord(latlng):
            return str(latlng)[1:-1]

        df_centroids = pd.DataFrame(centroids)
        df_centroids = df_centroids.rename(columns={0:'lng', 1:'lat'})
        df_centroids['latlng'] = list(zip(df_centroids['lat'], df_centroids['lng']))
        df_centroids['latlng'] = df_centroids['latlng'].map(stringCoord)
        df_centroids['json_response'] = ''
        df_centroids['address'] = ''

        # helper function for finding address approximation for latitude, longitude coordinates via GoogleMaps API

        def reverse_geocode(latlng):
            result = {}
            url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={}'
            request = url.format(latlng)
            data = requests.get(request).json()
            if len(data['results']) > 0:
                result = data['results'][0]
            return result

        latlng_list = df_centroids['latlng'].tolist()
        responses = []
        for latlng in latlng_list:
            time.sleep(1)
            responses.append(reverse_geocode(latlng))
        df_centroids['json_response'] = responses

        # helper function for parsing geocode json responses and concatenating address

        def parseAddress(geocode_data):
            if (not geocode_data is None) and ('formatted_address' in geocode_data):
                street_number, street_name, neighborhood, city, postcode = '','','','',''
                for component in geocode_data['address_components']:
                    if 'street_number' in component['types']:
                        street_number = component['long_name']
                    if 'route' in component['types']:
                        street_name = component['long_name']
                    if 'neighborhood' in component['types']:
                        neighborhood = component['long_name']
                    if 'locality' in component['types']:
                        city = component['long_name']
                    if 'postal_code' in component['types']:
                        postcode = component['long_name']
                return street_number + " " + street_name + ", " + neighborhood + ", " + postcode


        df_centroids['address'] = df_centroids['json_response'].map(parseAddress)

        df2['latlng'] = list(zip(df2['Latitude'], df2['Longitude']))
        df2['latlng'] = df2['latlng'].map(stringCoord)

        # helper function for retrieving distance matrix between crash point and all possible Boston EMS Stations. 

        def getDistanceMatrix(origin, destination):
            result = {}
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origin={}&destination={}'
            request = url.format(origin, destination)
            data = requests.get(request).json()
            if len(data['results']) > 0:
                result = data['results'][0]
            return result

        #df_centroids.drop('lng',axis=1,inplace=True)
        #df_centroids.drop('lat',axis=1,inplace=True)
        df_centroids.drop('latlng',axis=1,inplace=True)
        df_centroids.drop('json_response',axis=1,inplace=True)

        df_centroids.to_json('optimalEMSStationLocations.json', orient ='index')

        with open('optimalEMSStationLocations.json') as data_file:    
            all_data = json.load(data_file)

        repo['cfortuna_houset_karamy_snjan19.OptimalEMSStations'].insert(all_data)

        repo.logout()

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}

    """Provenance of this Document"""
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
        repo.authenticate('cfortuna_houset_karamy_snjan19', 'cfortuna_houset_karamy_snjan19')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')
        doc.add_namespace('mag', 'https://data.mass.gov/resource/')
        doc.add_namespace('car', 'http://datamechanics.io/data/cfortuna_houset_karamy_snjan19/')

        this_script = doc.agent('alg:cfortuna_houset_karamy_snjan19#optimalStations', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        

        carCrashResource = doc.entity('car:CarCrashData', {'prov:label':'Car Crash Data', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        emsResource = doc.entity('bdp:EMSStationsData', {'prov:label':'EMS Stations Data', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        optimalEMSStationsResource = doc.entity('dat:cfortuna_houset_karamy_snjan19#OptimalEMSStations', {'prov:label':'Optimal EMS Stations Data', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})

        getCarCrashData = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)  
        getEMSStationsData = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        getOptimalEMSStations = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(getCarCrashData, this_script)
        doc.wasAssociatedWith(getEMSStationsData, this_script)
        doc.wasAssociatedWith(getOptimalEMSStations, this_script)

        doc.usage(getCarCrashData, carCrashResource, startTime, None, {prov.model.PROV_TYPE:'ont:Retrieval'})
        doc.usage(getEMSStationsData, emsResource, startTime, None,{prov.model.PROV_TYPE:'ont:Retrieval',})
        doc.usage(getOptimalEMSStations, optimalEMSStationsResource, startTime, None,{prov.model.PROV_TYPE:'ont:Retrieval',})

        CarCrashData = doc.entity('dat:cfortuna_houset_karamy_snjan19#CarCrashData', {prov.model.PROV_LABEL:'Car Crash Data', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(CarCrashData, this_script)
        doc.wasGeneratedBy(CarCrashData, getCarCrashData, endTime)
        doc.wasDerivedFrom(CarCrashData, carCrashResource, getCarCrashData, getCarCrashData, getCarCrashData)

        EMSStationsData = doc.entity('dat:cfortuna_houset_karamy_snjan19#EMSStationsData', {prov.model.PROV_LABEL:'EMS Stations Data', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(EMSStationsData, this_script)
        doc.wasGeneratedBy(EMSStationsData, getEMSStationsData, endTime)
        doc.wasDerivedFrom(EMSStationsData, emsResource, getEMSStationsData, getEMSStationsData, getEMSStationsData)
        repo.logout()

        OptimalEMSStations = doc.entity('dat:cfortuna_houset_karamy_snjan19#OptimalEMSStations', {prov.model.PROV_LABEL:'Optimal EMS Stations', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(OptimalEMSStations, this_script)
        doc.wasGeneratedBy(OptimalEMSStations, getOptimalEMSStations, endTime)
        doc.wasDerivedFrom(OptimalEMSStations, optimalEMSStationsResource, getOptimalEMSStations, getOptimalEMSStations, getOptimalEMSStations)
        repo.logout()

        return doc

optimalEMSStations.execute()
#doc = OptimalHospitals.provenance()
#print(doc.get_provn())
# print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof
