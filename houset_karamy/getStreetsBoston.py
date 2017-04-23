import urllib.request
import json
import dml
import prov.model
import datetime
import uuid

class getStreetsBoston(dml.Algorithm):
    contributor = 'houset_karamy'
    reads = []
    writes = ['houset_karamy.streetsBoston']

    @staticmethod
    def execute(trial = False):
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('houset_karamy', 'houset_karamy')
        
        dataSets = {'streetsBoston': 'http://data.mass.gov/resource/ms23-5ubn.json'}  
        for ds in dataSets:
            url = dataSets[ds]
            response = urllib.request.urlopen(url).read().decode("utf-8")
            r = json.loads(response)
            s = json.dumps(r, sort_keys=True, indent=2)
            repo.dropPermanent(ds)
            repo.createPermanent(ds)
            repo['houset_karamy.' + ds].insert_many(r)
        
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
        repo.authenticate('houset_karamy', 'houset_karamy')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')
        doc.add_namespace('mag', 'https://data.mass.gov/resource/')
        
        this_script = doc.agent('alg:houset_karamy#streetsBoston', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        
        resource1 = doc.entity('mag:ms23-5ubn', {'prov:label':'Streets Boston', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
                        
        get_streetsBoston = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
 
        doc.wasAssociatedWith(get_streetsBoston, this_script)
        
        doc.usage(get_streetsBoston, resource1, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'})
           
        streetsBoston = doc.entity('dat:houset_karamy#streetsBoston', {prov.model.PROV_LABEL:'Streets Boston', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(streetsBoston, this_script)
        doc.wasGeneratedBy(streetsBoston, get_streetsBoston, endTime)
        doc.wasDerivedFrom(streetsBoston, resource1, get_streetsBoston, get_streetsBoston, get_streetsBoston) 
        

        repo.logout()
                  
        return doc


#get.execute()
#doc = get.provenance()
#print(doc.get_provn())
#print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof
