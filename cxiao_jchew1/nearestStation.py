# nearestStation.py
# Data Mechanics
# Finds the nearest police station for each crime report in Boston

import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import math

class mergeCrime(dml.Algorithm):
    contributor = 'cxiao_jchew1'
    reads = ['cxiao_jchew1.crime_reports', 'cxiao_jchew1.police_stations']
    writes = ['cxiao_jchew1.crime_police_near']

    @staticmethod
    def execute(trial = False):        
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('cxiao_jchew1', 'cxiao_jchew1')

        # loads collection
        CR = repo['cxiao_jchew1.crime_reports'].find()
        PR = repo['cxiao_jchew1.police_stations'].find()

        crimeX = []
        crimeY = []
        policeX = []
        policeY = []

        for i in CR:
            try:
                crimeX.append(i['long'])
                crimeY.append(i['lat'])
            except:
                pass

        for i in PR:
            try:
                policeX.append(i['centroidx'])
                policeY.append(i['centroidy'])
            except:
                pass

        floatCrimeX = [float(x) for x in crimeX]
        floatCrimeY = [float(y) for y in crimeY]
        floatPoliceX = [float(x) for x in policeX]
        floatPoliceY = [float(y) for y in policeY]

        L1 = []
        L2 = []
        L3 = []
        L4 = []
        L5 = []
        L6 = []
        L7 = []
        L8 = []
        L9 = []
        L10 = []
        L11 = []
        L12 = []

        for i in range(0, len(floatCrimeX)):
            count = 0
            minDistance = 100
            for j in range(0, len(floatPoliceX)):
                'Each crime report calculates its distance from each police station and'
                'finds the closest police station to that crime report'
                dist1 = abs(floatCrimeX[i] - floatPoliceX[j])
                dist2 = abs(floatCrimeY[i] - floatPoliceY[j])
                avg = (dist1 + dist2) / 2.0
                if(avg < minDistance):
                    minDistance = avg
                    count = j
            if(count == 0):
                L1.append(floatCrimeX[i])
            if(count == 1):
                L2.append(floatCrimeX[i])
            if(count == 2):
                L3.append(floatCrimeX[i])
            if(count == 3):
                L4.append(floatCrimeX[i])
            if(count == 4):
                L5.append(floatCrimeX[i])
            if(count == 5):
                L6.append(floatCrimeX[i])
            if(count == 6):
                L7.append(floatCrimeX[i])
            if(count == 7):
                L8.append(floatCrimeX[i])
            if(count == 8):
                L9.append(floatCrimeX[i])
            if(count == 9):
                L10.append(floatCrimeX[i])
            if(count == 10):
                L11.append(floatCrimeX[i])
            if(count == 11):
                L12.append(floatCrimeX[i])

        print("District A-1 Police Station:")
        print(len(L1))
        print("District D-4 Police Station:")
        print(len(L2))
        print("District E-13 Police Station:")
        print(len(L3))
        print("District B-3 Police Station:")
        print(len(L4))
        print("District E-18 Police Station:")
        print(len(L5))
        print("District D-14 Police Station:")
        print(len(L6))
        print("Boston Police Headquarters:")
        print(len(L7))
        print("District A-7 Police Station:")
        print(len(L8))
        print("District C-6 Police Station:")
        print(len(L9))
        print("District B-2 Police Station:")
        print(len(L10))
        print("District E-5 Police Station:")
        print(len(L11))
        print("District C-11 Police Station:")
        print(len(L12))

        repo.logout()

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}

    @staticmethod
    def provenance(doc=prov.model.ProvDocument(), startTime=None, endTime=None):
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
            '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('cxiao_jchew1', 'cxiao_jchew1')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/')  # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/')  # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont',
                          'http://datamechanics.io/ontology#')  # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/')  # The event log.

        this_script = doc.agent('alg:cxiao_jchew1#nearestStation',
                                {prov.model.PROV_TYPE: prov.model.PROV['SoftwareAgent'], 'ont:Extension': 'py'})
        resource_crimeReports = doc.entity('dat:cxiao_jchew1#crime_reports',
                                             {'prov:label': 'Crime Reports',
                                              prov.model.PROV_TYPE: 'ont:DataSet'})
        resource_policeStations = doc.entity('dat:cxiao_jchew1#police_stations',
                                             {'prov:label': 'Police Stations',
                                              prov.model.PROV_TYPE: 'ont:DataSet'})

        get_nearStation = doc.activity('log:uuid' + str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(get_nearStation, this_script)
        doc.usage(get_nearStation, resource_crimeReports, startTime, None,
                  {prov.model.PROV_TYPE: 'ont:Computation'})
        doc.usage(get_nearStation, resource_policeStations, startTime, None,
                  {prov.model.PROV_TYPE: 'ont:Computation'})

        nearStation = doc.entity('dat:cxiao_jchew1#crime_police_near',
                          {prov.model.PROV_LABEL: 'Nearest Station',
                           prov.model.PROV_TYPE: 'ont:DataSet'})
        doc.wasAttributedTo(nearStation, this_script)
        doc.wasGeneratedBy(nearStation, get_nearStation, endTime)
        doc.wasDerivedFrom(nearStation, resource_crimeReports, get_nearStation, get_nearStation, get_nearStation)
        doc.wasDerivedFrom(nearStation, resource_policeStations, get_nearStation, get_nearStation, get_nearStation)
        
        repo.logout()

        return doc

mergeCrime.execute()
doc = mergeCrime.provenance()

## eof
