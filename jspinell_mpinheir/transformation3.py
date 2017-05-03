import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import dataManipulation as dm

class transformation3(dml.Algorithm):
    contributor = 'jspinell_mpinheir'
    reads = ['jspinell_mpinheir.ageRanges',
             'jspinell_mpinheir.housingRates',
             'jspinell_mpinheir.neighborhoods']
    writes = ['jspinell_mpinheir.ageByTier']

    @staticmethod
    def execute(trial = False):
        startTime = datetime.datetime.now()
    
        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('jspinell_mpinheir', 'jspinell_mpinheir')

        ageRanges = list(repo.jspinell_mpinheir.ageRanges.find())
        housingRates = list(repo.jspinell_mpinheir.housingRates.find())
        neighborhoods = list(repo.jspinell_mpinheir.neighborhoods.find())
        
        #Break housing prices into tiers
        typesOfHomes = ["Average Rent 2 Bedroom"]
        housingTiers = dm.createTiers(housingRates, typesOfHomes, 5)
        
        #Pull zips with population info on 15 to 19 years of age
        
        newAgeRanges = dm.pullAges(ageRanges, "Zip ", "15_to_19_years")
        #print(newAgeRanges)
        #Isolate Zips with a certain home
        zipAndRent = dm.zipToRent(housingRates, typesOfHomes)
        
        
        #Assign Tiers
        zipAndTier = dm.assignTier(zipAndRent, housingTiers, typesOfHomes)
        
        #MapReduce Tiers to average population of 15 to 19 year olds in that Tier
        zipAndTier = [(k,v) for i in range(len(zipAndTier)) for k,v in zipAndTier[i].items()]
        newAgeRanges = [(k,v) for i in range(len(newAgeRanges)) for k,v in newAgeRanges[i].items()]
        
        mapped = [(a[1], b[1]) for a in zipAndTier for b in newAgeRanges if a[0] == b[0]]
        
        reduced = dm.reduce(lambda k,v:(k,sum(v)/len(v)), mapped)
        reduced.sort()
        toPush = [{"Price Range":str(reduced[i][0]) + "-" + str(reduced[i+1][0]), 
        "Average Age":str(reduced[i][1])} for i in range(len(reduced) - 1)]
    
        repo.dropCollection('ageByTier')
        repo.createCollection('ageByTier')
        repo['jspinell_mpinheir.ageByTier'].insert_many(toPush)
        
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
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')

        this_script = doc.agent('alg:jspinell_mpinheir#transformation3', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        ageByTier = doc.entity('dat:jspinell_mpinheir#ageRanges', {prov.model.PROV_LABEL:'Age By Tier', prov.model.PROV_TYPE:'ont:DataSet'})
        this_ageByTier = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        
        doc.wasAssociatedWith(this_ageByTier, this_script)
        
        doc.used(this_ageByTier, ageByTier, startTime)
        doc.wasAttributedTo(ageByTier, this_script)
        doc.wasGeneratedBy(ageByTier, this_ageByTier, endTime)
        
        #repo.record(doc.serialize())

        repo.logout()
                  
        return doc
    
"""
transformation3.execute()
doc = transformation3.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))
"""

## eof
