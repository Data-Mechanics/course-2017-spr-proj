import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import dataManipulation as dm

class transformation2(dml.Algorithm):
    contributor = 'jspinell_mpinheir'
    reads = ['jspinell_mpinheir.educationCosts',
             'jspinell_mpinheir.housingRates',
             'jspinell_mpinheir.neighborhoods']
    writes = ['jspinell_mpinheir.educationByTier']

    @staticmethod
    def execute(trial = False):
        startTime = datetime.datetime.now()
    
        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('jspinell_mpinheir', 'jspinell_mpinheir')

        educationCosts = list(repo.jspinell_mpinheir.educationCosts.find())
        housingRates = list(repo.jspinell_mpinheir.housingRates.find())
        neighborhoods = list(repo.jspinell_mpinheir.neighborhoods.find())
        
        #Break housing prices into tiers
        typesOfHomes = ["Average Rent 2 Bedroom"]
        housingTiers = dm.createTiers(housingRates, typesOfHomes, 5)
        
        #Pull 4-year College Grad Rates from each Zip
        
        gradRates = dm.pullGrad(educationCosts, "Zip ", "College Grad Rate")
        #newNeighborhoods = pullNeighborhood(neighborhoods, "Zip ", "Neighborhood")
        #print(educationCosts)
        #print(gradRates)
        #print(newNeighborhoods)
        #Isolate Zips with a certain home
        zipAndRent = dm.zipToRent(housingRates, typesOfHomes)
        
        
        #Assign Tiers
        zipAndTier = dm.assignTier(zipAndRent, housingTiers, typesOfHomes)
    
        #MapReduce Tiers to average grad rate in that tier
        zipAndTier = [(k,v) for i in range(len(zipAndTier)) for k,v in zipAndTier[i].items()]
        #print(zipAndTier)
        newGradRates = [(k,v) for i in range(len(gradRates)) for k,v in gradRates[i].items()]
        
        mapped = [(a[1], b[1]) for a in zipAndTier for b in newGradRates if a[0] == b[0]]
        
        #print(mapped)
        #print(tierToMax)
        
        reduced = dm.reduce(lambda k,v:(k,sum(v)/len(v)), mapped)
        reduced.sort()
        toPush = [{"Price Range":str(reduced[i][0]) + "-" + str(reduced[i+1][0]), 
        "Education Cost":str(reduced[i][1])} for i in range(len(reduced) - 1)]
    
        repo.dropCollection('educationByTier')
        repo.createCollection('educationByTier')
        repo['jspinell_mpinheir.educationByTier'].insert_many(toPush)
        
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
        

        this_script = doc.agent('alg:jspinell_mpinheir#transformation2', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        educationByTier = doc.entity('dat:jspinell_mpinheir#educationCosts', {prov.model.PROV_LABEL:'Education By Tier', prov.model.PROV_TYPE:'ont:DataSet'})
        this_educationByTier = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        
        doc.wasAssociatedWith(this_educationByTier, this_script)
        
        doc.used(this_educationByTier, educationByTier, startTime)
        doc.wasAttributedTo(educationByTier, this_script)
        doc.wasGeneratedBy(educationByTier, this_educationByTier, endTime)
        
        #repo.record(doc.serialize())

        repo.logout()
                  
        return doc
    
"""
transformation2.execute()
doc = transformation2.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))
"""

## eof