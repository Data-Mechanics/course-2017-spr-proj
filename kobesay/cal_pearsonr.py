import urllib.request
import json
import dml
import prov.model
import datetime
import uuid

from random import shuffle
from math import sqrt

def permute(x):
    shuffled = [xi for xi in x]
    shuffle(shuffled)
    return shuffled

def avg(x): # Average
    return sum(x)/len(x)

def stddev(x): # Standard deviation.
    m = avg(x)
    return sqrt(sum([(xi-m)**2 for xi in x])/len(x))

def cov(x, y): # Covariance.
    return sum([(xi-avg(x))*(yi-avg(y)) for (xi,yi) in zip(x,y)])/len(x)

def corr(x, y): # Correlation coefficient.
    if stddev(x)*stddev(y) != 0:
        return cov(x, y)/(stddev(x)*stddev(y))

def p(x, y):
    c0 = corr(x, y)
    corrs = []
    for k in range(0, 2000):
        y_permuted = permute(y)
        corrs.append(corr(x, y_permuted))
    return len([c for c in corrs if abs(c) > c0])/len(corrs)

class cal_pearsonr(dml.Algorithm):
    contributor = 'kobesay'
    reads = [
        'kobesay.income_infrastructure'
    ]
    writes = [
        'kobesay.income_infrastructure_pearsonr'
    ]

    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('kobesay', 'kobesay')

        repo.dropCollection("income_infrastructure_pearsonr")
        repo.createCollection("income_infrastructure_pearsonr")

        income_infrastructure = repo.kobesay.income_infrastructure.find()
        income_infrastructure = [x for x in income_infrastructure]

        income = [x['income'] for x in income_infrastructure]
        num_hospital = [x['num_hospital'] for x in income_infrastructure]
        num_school = [x['num_school'] for x in income_infrastructure]
        num_publicschool = [x['num_publicschool'] for x in income_infrastructure]
        num_nonpublicschool = [x['num_nonpublicschool'] for x in income_infrastructure]

        pearsonr_income_hospital = corr(income, num_hospital)
        pearsonr_income_school = corr(income, num_school)
        pearsonr_income_publicschool = corr(income, num_publicschool)
        pearsonr_income_nonpublicschool = corr(income, num_nonpublicschool)
        r = [
            {
                "income_hospital": pearsonr_income_hospital,
                "income_school": pearsonr_income_school,
                "income_publicschool": pearsonr_income_publicschool,
                "income_nonpublicschool": pearsonr_income_nonpublicschool
            }
        ]
        repo['kobesay.income_infrastructure_pearsonr'].insert_many(r)
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
        repo.authenticate('kobesay', 'kobesay')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/') # City of Boston Data Portal
        doc.add_namespace('bwod', 'https://boston.opendatasoft.com/explore/dataset/') # Boston Wicked Open Data
        doc.add_namespace('bod', 'http://bostonopendata.boston.opendata.arcgis.com/datasets/') # BostonMaps: Open Data

        this_script = doc.agent('alg:kobesay#cal_pearsonr', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        income_infrastructure = doc.entity('dat:kobesay#income_infrastructure', {'prov:label':'region income and infrastructure', prov.model.PROV_TYPE:'ont:DataSet'})
        cal_pearsonr = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime, {'prov:label':'calculate pearson correlation coefficient on region income and infrastructure'})
        doc.wasAssociatedWith(cal_pearsonr, this_script)

        income_infrastructure_pearsonr = doc.entity('dat:kobesay#income_infrastructure_pearsonr', {prov.model.PROV_LABEL:'pearson correlation coefficient on region income and infrastructure', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(income_infrastructure_pearsonr, this_script)
        doc.wasGeneratedBy(income_infrastructure_pearsonr, cal_pearsonr, endTime)
        doc.wasDerivedFrom(income_infrastructure_pearsonr, income_infrastructure, cal_pearsonr, cal_pearsonr, cal_pearsonr)

        repo.logout()
                  
        return doc

"""
# TEST
cal_pearsonr.execute()
doc = cal_pearsonr.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))
"""