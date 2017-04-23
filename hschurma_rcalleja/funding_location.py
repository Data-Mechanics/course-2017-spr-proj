import urllib.request
import json
import dml
import prov.model
import datetime
import uuid

def union(R, S):
    return R + S

def difference(R, S):
    return [t for t in R if t not in S]

def intersect(R, S):
    return [t for t in R if t in S]

def project(R, p):
    return [p(t) for t in R]

def select(R, s):
    return [t for t in R if s(t)]
 
def product(R, S):
    return [(t,u) for t in R for u in S]

def aggregate(R, f):
    keys = {r[0] for r in R}
    return [(key, f([v for (k,v) in R if k == key])) for key in keys]

class funding_location(dml.Algorithm):
    contributor = 'hschurma_rcalleja'
    reads = ['hschurma_rcalleja.funding', 'hschurma_rcalleja.location']
    writes = ['hschurma_rcalleja.location_funding']


    @staticmethod
    def execute(trial = False):
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('hschurma_rcalleja', 'hschurma_rcalleja')

        repo.dropPermanent("location_funding")
        repo.createPermanent("location_funding")

        #size of location data set
        size = list(repo.hschurma_rcalleja.location.aggregate([{"$project": { "item":1, "numberOfSchools": { "$size": "$data"}}}]))
        s = size[0]['numberOfSchools']

        #list of schools
        schools = []
        for i in range(s):
            schools.append(list(repo.hschurma_rcalleja.location.aggregate([{"$project": { "school": { "$arrayElemAt": ["$data", i]}}}])))


        #print(schools[0][0]['school'][12][0]['zip'])
        #filter just name and location of schools
        nameLoc = []
        for j in range(s):
            if schools[j][0]['school'][11] =="HS" or schools[j][0]['school'][11] =="6th-12" or schools[j][0]['school'][11] =="Mary 9-12":
                sch = json.loads(schools[0][0]['school'][12][0])
                nameLoc.append({'Name': schools[j][0]['school'][10], 'location': [sch['zip'], schools[j][0]['school'][12][1:3]]})



        
        #Dict of School name and Funding
        funding = list(repo.hschurma_rcalleja.funding.aggregate([{"$project":{"_id":0}}]))
        
        nameFund = []
        for f in funding:
            nameFund.append({'Name': f['School Name'].strip(), 'Funding': {'2008': f['2008_All'].strip(),'2009': f['2009_All'].strip(),'2010': f['2010_All'].strip(),'2011': f['2011_All'].strip(),'2012': f['2012_All'].strip(),'2013': f['2013_All'].strip(),'2014': f['2014_All'].strip(),'2015': f['2015_All'].strip(),'2016': f['2016_All'].strip()}})



        P = product(nameLoc, nameFund)
        #print(P)
        S = select(P, lambda t: t[0]['Name'] == t[1]['Name'])
        #print(S)
        PR = project(S, lambda t: {'Name': t[0]['Name'], 'location': t[0]['location'], 'Funding': t[1]['Funding']})
        #print(PR)
        
        repo.dropCollection('funding_location')
        repo.createCollection('funding_location')
        repo['hschurma_rcalleja.funding_location'].insert(PR)
    

    @staticmethod
    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        '''Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.'''
        

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('hschurma_rcalleja', 'hschurma_rcalleja')

        
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')


        this_script = doc.agent('alg:hschurma_rcalleja#location_funding', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})


        location = doc.entity('dat:hschurma_rcalleja#location', {prov.model.PROV_LABEL:'Boston Public Schools', \
            prov.model.PROV_TYPE:'ont:DataSet'})
        funding = doc.entity('dat:hschurma_rcalleja#funding',{prov.model.PROV_LABEL:'BPS Funding', \
            prov.model.PROV_TYPE:'ont:DataSet'})


        
        get_loc_fund = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_loc_fund, this_script)
        
        doc.used(get_loc_fund, location, startTime)
        doc.used(get_loc_fund, funding, startTime)

        loc_fund = doc.entity('dat:hschurma_rcalleja#location_funding', {prov.model.PROV_LABEL:'High School Funding and Location Data', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(loc_fund, this_script)
        doc.wasGeneratedBy(loc_fund, get_loc_fund, endTime)

        doc.wasDerivedFrom(loc_fund, funding, get_loc_fund, get_loc_fund, get_loc_fund)
        doc.wasDerivedFrom(loc_fund, location, get_loc_fund, get_loc_fund, get_loc_fund)

        repo.record(doc.serialize())
        repo.logout()
                  
        return doc
        
funding_location.execute()
'''doc = funding_location.provenance()
print(json.dumps(json.loads(doc.serialize()), indent=4))'''

        
