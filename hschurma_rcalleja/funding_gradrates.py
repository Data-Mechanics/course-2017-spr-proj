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

def prodThree(R, S, T):
    return [(t,u,v) for t in R for u in S for v in T]

def aggregate(R, f):
    keys = {r[0] for r in R}
    return [(key, f([v for (k,v) in R if k == key])) for key in keys]

class funding_gradrates(dml.Algorithm):
    contributor = 'hschurma_rcalleja'
    reads = ['hschurma_rcalleja.funding', 'hschurma_rcalleja.gradrates', 'hschurma_rcalleja.graduation']
    writes = ['hschurma_rcalleja.funding_gradrates']


    @staticmethod
    def execute(trial = False):
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('hschurma_rcalleja', 'hschurma_rcalleja')

        repo.dropPermanent("funding_gradrates")
        repo.createPermanent("funding_gradrates")
        
        #Dict of School name and Funding
        funding = list(repo.hschurma_rcalleja.funding.aggregate([{"$project":{"_id":0}}]))

        #print(funding)
        nameFund = []

        for f in funding:
            nameFund.append({'Name': f['School Name'].strip(), 'Funding': {'2008': f['2008_All'].strip(),'2009': f['2009_All'].strip(),'2010': f['2010_All'].strip(),'2011': f['2011_All'].strip(),'2012': f['2012_All'].strip(),'2013': f['2013_All'].strip(),'2014': f['2014_All'].strip(),'2015': f['2015_All'].strip(),'2016': f['2016_All'].strip()}})


        '''
        #create list of (school name, funding)
        nameFund = []
        for i in range(len(funding)):
            nameFund.append({'Name': funding[i]["FIELD2"].strip(), 'Funding': funding[i]["FIELD13"].strip()})

        #list size of graduation data
        size = list(repo.hschurma_rcalleja.graduation.aggregate([{"$project": { "item":1, "numEntries": { "$size": "$data"}}}]))
        s = size[0]['numEntries']

        #create list of (school name, num students graduated)
        grads = []
        schools = []
        for i in range(s):
            school = list(repo.hschurma_rcalleja.graduation.aggregate([{"$project": { "school": { "$arrayElemAt": ["$data", i]}}}]))
            if (school[0]['school'][13] == "All Colleges" and school[0]['school'][14] == "All Students"):
                grads.append({'Name': school[0]['school'][12], 'GradNum': school[0]['school'][15]})
        '''
        
        #list of grad rates
        gradrates = list(repo.hschurma_rcalleja.gradrates.aggregate([{"$project":{"_id":0, "FIELD1":1, "2008":1, "2009":1, "2010":1, "2011":1, "2012":1, "2013":1, "2014":1, "2015":1, "2016":1}}]))

        #project into list of (school name, grad rate)
        name_grad = []
        for i in gradrates:
            name_grad.append({'Name': i['FIELD1'], 'GradRates': {'2008':i['2008'], '2009':i['2009'], '2010':i['2010'], '2011':i['2011'], '2012':i['2012'], '2013':i['2013'], '2014':i['2014'], '2015':i['2015'], '2016':i['2016']}})

        
        
        P = product(name_grad, nameFund)
        S = select(P, lambda t: t[0]['Name'] == t[1]['Name'])
        PR = project(S, lambda t: {'Name': t[0]['Name'], 'Funding': t[1]['Funding'], 'Graduation Rates': t[0]['GradRates']})

        #database collection containing 'Name', 'Funding' {2008... 2016}, 'Grad Rates' {2008...2016}
    
        repo.dropCollection('funding_gradrates')
        repo.createCollection('funding_gradrates')
        repo['hschurma_rcalleja.funding_gradrates'].insert(PR)
        
        
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
    
        this_script = doc.agent('alg:hschurma_rcalleja#funding_gradrates', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})

        funding = doc.entity('dat:hschurma_rcalleja#funding', {'prov:label':'BPS Funding', \
            prov.model.PROV_TYPE:'ont:DataSet'})
        gradrates = doc.entity('dat:hschurma_rcalleja#gradrates', {'prov:label':'BPS Graduation Rates', \
            prov.model.PROV_TYPE:'ont:DataSet'})
        gradnums = doc.entity('dat:hschurma_rcalleja#graduation', {'prov:label':'Graduates Attending College', \
            prov.model.PROV_TYPE:'ont:DataSet'})
        
        get_grad_fund = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_grad_fund, this_script)

        doc.used(get_grad_fund, funding, startTime)
        doc.used(get_grad_fund, gradrates, startTime)
        doc.used(get_grad_fund, gradnums, startTime)

        grad_fund = doc.entity('dat:hschurma_rcalleja#funding_gradrates', {prov.model.PROV_LABEL:'High School Funding and Graduation Data', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(grad_fund, this_script)
        doc.wasGeneratedBy(grad_fund, get_grad_fund, endTime)
        
        doc.wasDerivedFrom(grad_fund, funding, get_grad_fund, get_grad_fund, get_grad_fund)
        doc.wasDerivedFrom(grad_fund, gradrates, get_grad_fund, get_grad_fund, get_grad_fund)
        doc.wasDerivedFrom(grad_fund, gradnums, get_grad_fund, get_grad_fund, get_grad_fund)

        repo.record(doc.serialize())
        repo.logout()
                  
        return doc
        
funding_gradrates.execute()
#doc = funding_gradrates.provenance()
#print(doc.get_provn())
#print(json.dumps(json.loads(doc.serialize()), indent=4))

