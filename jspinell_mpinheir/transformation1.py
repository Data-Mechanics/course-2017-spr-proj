import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import dataManipulation as dm

class transformation1(dml.Algorithm):
    contributor = 'jspinell_mpinheir'
    reads = ['jspinell_mpinheir.crimeRate',
             'jspinell_mpinheir.housingRates',
             'jspinell_mpinheir.neighborhoods']
    writes = ['jspinell_mpinheir.crimeByTier']

    @staticmethod
    def execute(trial = False):
        startTime = datetime.datetime.now()
    
        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('jspinell_mpinheir', 'jspinell_mpinheir')
        
        crimeRate = list(repo.jspinell_mpinheir.crimeRate.find())
        housingRates = list(repo.jspinell_mpinheir.housingRates.find())
        neighborhoods = list(repo.jspinell_mpinheir.neighborhoods.find())
        
        #Break housing prices into tiers
        typesOfHomes = ["Average Rent 2 Bedroom"]
        housingTiers = dm.createTiers(housingRates, typesOfHomes, 5)
        
        #Normalize Crime Score for Boston & Cambridge
        newCrimeRate = dm.normalizeDict(crimeRate, "Zip Code", "Crime Risk Index")

        #Isolate Zips with a certain home
        zipAndRent = dm.zipToRent(housingRates, typesOfHomes)
        
        
        #Assign Tiers
        zipAndTier = dm.assignTier(zipAndRent, housingTiers, typesOfHomes)
        
        zipAndTier = [(k,v) for i in range(len(zipAndTier)) for k,v in zipAndTier[i].items()]
        newCrimeRate = [(k,v) for i in range(len(newCrimeRate)) for k,v in newCrimeRate[i].items()]
        mapped = [(a[1], b[1]) for a in zipAndTier for b in newCrimeRate if a[0] == b[0]]
        
        reduced = dm.reduce(lambda k,v:(k,sum(v)/len(v)), mapped)
        reduced.sort()
        toPush = [{"Price Range":str(reduced[i][0]) + "-" + str(reduced[i+1][0]), 
        "Crime Rate":str(reduced[i][1])} for i in range(len(reduced) - 1)]
    
        repo.dropCollection('crimeByTier')
        repo.createCollection('crimeByTier')
        repo['jspinell_mpinheir.crimeByTier'].insert_many(toPush)
        
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
        repo.authenticate('jspinell_mpinheir', 'jspinell_mpinheir')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        

        this_script = doc.agent('alg:jspinell_mpinheir#transformation1', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        crimeByTier = doc.entity('dat:jspinell_mpinheir#crimeRates', {prov.model.PROV_LABEL:'Crime By Tier', prov.model.PROV_TYPE:'ont:DataSet'})
        this_crimeByTier = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        
        doc.wasAssociatedWith(this_crimeByTier, this_script)
        
        doc.used(this_crimeByTier, crimeByTier, startTime)
        doc.wasAttributedTo(crimeByTier, this_script)
        doc.wasGeneratedBy(crimeByTier, this_crimeByTier, endTime)
        
        #repo.record(doc.serialize())

        repo.logout()
                  
        return doc
    
"""
transformation1.execute()
doc = transformation1.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))
"""

## eof