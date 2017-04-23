import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import csv
import json
import requests 

class retrieveData(dml.Algorithm):
    contributor = 'cfortuna_houset_karamy_snjan19'
    reads = []
    writes = ['cfortuna_houset_karamy_snjan19.CarCrashData','cfortuna_houset_karamy_snjan19.BostonHospitalsData','cfortuna_houset_karamy_snjan19.EMSStationsData']

    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('cfortuna_houset_karamy_snjan19', 'cfortuna_houset_karamy_snjan19')

        ###### Importing Datasets and putting them inside the mongoDB database #####



        # Boston Hospitals
        url = 'http://data.cityofboston.gov/resource/u6fv-m8v4.json'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r = json.loads(response)
        s = json.dumps(r, sort_keys=True, indent=2)
        repo.dropCollection("BostonHospitalsData")
        repo.createCollection("BostonHospitalsData")
        repo['cfortuna_houset_karamy_snjan19.BostonHospitalsData'].insert_many(r)

        # EMS Stations
        url = 'http://datamechanics.io/data/cfortuna_houset_karamy_snjan19/EMSStationsData.json'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r = json.loads(response)
        s = json.dumps(r, sort_keys=True, indent=2)
        repo.dropCollection("EMSStationsData")
        repo.createCollection("EMSStationsData")
        repo['cfortuna_houset_karamy_snjan19.EMSStationsData'].insert_many(r)

        # Car Crashes
        url = 'http://datamechanics.io/data/cfortuna_houset_karamy_snjan19/CarCrashData.json'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r = json.loads(response)
        s = json.dumps(r, sort_keys=True, indent=2)
        repo.dropCollection("CarCrashData")
        repo.createCollection("CarCrashData")
        repo['cfortuna_houset_karamy_snjan19.CarCrashData'].insert_many(r)

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
        repo.authenticate('cfortuna_houset_karamy_snjan19', 'cfortuna_houset_karamy_snjan19')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')
        doc.add_namespace('mag', 'https://data.mass.gov/resource/')
        doc.add_namespace('car', 'http://datamechanics.io/data/cfortuna_houset_karamy_snjan19/')

        this_script = doc.agent('alg:cfortuna_houset_karamy_snjan19#retrieveData', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        
        #streetResource = doc.entity('mag:ms23-5ubn', {'prov:label':'Boston Streets Data', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        #wazeResource = doc.entity('bdp:dih6-az4h', {'prov:label':'Waze Traffic Data', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        hospitalsResource = doc.entity('bdp:u6fv-m8v4', {'prov:label':'Boston Hospitals Data', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        carCrashResource = doc.entity('car:CarCrashData', {'prov:label':'Car Crash Data', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        emsStationsResource = doc.entity('car:EMSStationsData', {'prov:label':'EMS Stations Data', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        
        #getBostonStreetsData = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        #getWazeTrafficData = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        getBostonHospitalsData = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        getCarCrashData = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        getEMSStationsData = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        
        #doc.wasAssociatedWith(getBostonStreetsData, this_script)
        #doc.wasAssociatedWith(getWazeTrafficData, this_script)
        doc.wasAssociatedWith(getBostonHospitalsData, this_script)
        doc.wasAssociatedWith(getCarCrashData, this_script)
        doc.wasAssociatedWith(getEMSStationsData, this_script)

        # doc.usage(getBostonStreetsData, streetResource, startTime, None,
        #           {prov.model.PROV_TYPE:'ont:Retrieval',
        #           #'ont:Query':'?type=Neighborhood+Area+Cambridge'
        #           }
        #          )
        # doc.usage(getWazeTrafficData, wazeResource, startTime, None,
        #           {prov.model.PROV_TYPE:'ont:Retrieval',
        #           #'ont:Query':'?type=Neighborhood+Area+Boston'
        #           }
        #           )
        doc.usage(getBostonHospitalsData, hospitalsResource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',
                  #'ont:Query':'?type=Neighborhood+Area+Cambridge'
                  }
                  )
        doc.usage(getCarCrashData, carCrashResource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',
                  #'ont:Query':'?type=Neighborhood+Area+Cambridge'
                  }
                  )
        doc.usage(getEMSStationsData, emsStationsResource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',
                  #'ont:Query':'?type=Neighborhood+Area+Cambridge'
                  }
                  )

        # BostonStreetsData = doc.entity('dat:cfortuna_houset_karamy_snjan19#BostonStreetsData', {prov.model.PROV_LABEL:'Boston Streets Data', prov.model.PROV_TYPE:'ont:DataSet'})
        # doc.wasAttributedTo(BostonStreetsData, this_script)
        # doc.wasGeneratedBy(BostonStreetsData, getBostonStreetsData, endTime)
        # doc.wasDerivedFrom(BostonStreetsData, streetResource, getBostonStreetsData, getBostonStreetsData, getBostonStreetsData)
        # WazeTrafficData = doc.entity('dat:cfortuna_houset_karamy_snjan19#WazeTrafficData', {prov.model.PROV_LABEL:'Waze Traffic Data', prov.model.PROV_TYPE:'ont:DataSet'})
        # doc.wasAttributedTo(WazeTrafficData, this_script)
        # doc.wasGeneratedBy(WazeTrafficData, getWazeTrafficData, endTime)
        # doc.wasDerivedFrom(WazeTrafficData, wazeResource, getWazeTrafficData, getWazeTrafficData, getWazeTrafficData)

        BostonHospitalsData = doc.entity('dat:cfortuna_houset_karamy_snjan19#BostonHospitalsData', {prov.model.PROV_LABEL:'Boston Hospitals Data', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(BostonHospitalsData, this_script)
        doc.wasGeneratedBy(BostonHospitalsData, getBostonHospitalsData, endTime)
        doc.wasDerivedFrom(BostonHospitalsData, hospitalsResource, getBostonHospitalsData, getBostonHospitalsData, getBostonHospitalsData)

        CarCrashData = doc.entity('dat:cfortuna_houset_karamy_snjan19#CarCrashData', {prov.model.PROV_LABEL:'Car Crash Data', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(CarCrashData, this_script)
        doc.wasGeneratedBy(CarCrashData, getCarCrashData, endTime)
        doc.wasDerivedFrom(CarCrashData, carCrashResource, getCarCrashData, getCarCrashData, getCarCrashData)

        EMSStationsData = doc.entity('dat:cfortuna_houset_karamy_snjan19#EMSStationsData', {prov.model.PROV_LABEL:'EMS Stations Data', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(EMSStationsData, this_script)
        doc.wasGeneratedBy(EMSStationsData, getEMSStationsData, endTime)
        doc.wasDerivedFrom(EMSStationsData, emsStationsResource, getEMSStationsData, getEMSStationsData, getEMSStationsData)

        repo.logout()
                  
        return doc

retrieveData.execute()
