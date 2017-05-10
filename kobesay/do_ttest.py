import urllib.request
import json
import dml
import prov.model
import datetime
import uuid

from scipy import stats

def avg(x): # Average
    return sum(x)/len(x)

class do_ttest(dml.Algorithm):
    contributor = 'kobesay'
    reads = [
        'kobesay.income_infrastructure'
    ]
    writes = [
        'kobesay.income_infrastructure_ttest'
    ]

    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('kobesay', 'kobesay')

        repo.dropCollection("income_infrastructure_ttest")
        repo.createCollection("income_infrastructure_ttest")

        income_infrastructure = repo.kobesay.income_infrastructure.find()
        income_infrastructure = [x for x in income_infrastructure]

        ordered = sorted(income_infrastructure, key=lambda x: x['income'], reverse=True)
        mid = int(len(ordered)/2)
        higher = ordered[0:mid]
        lower = ordered[mid:]

        higher_hospital = [x['num_hospital'] for x in higher]
        higher_school = [x['num_school'] for x in higher]
        higher_publicschool = [x['num_publicschool'] for x in higher]
        higher_nonpublicschool = [x['num_nonpublicschool'] for x in higher]

        lower_hospital = [x['num_hospital'] for x in lower]
        lower_school = [x['num_school'] for x in lower]
        lower_publicschool = [x['num_publicschool'] for x in lower]
        lower_nonpublicschool = [x['num_nonpublicschool'] for x in lower]

        hospital_tscore, hospital_pvalue = stats.ttest_ind(higher_hospital, lower_hospital)
        school_tscore, school_pvalue = stats.ttest_ind(higher_school, lower_school)
        publicschool_tscore, publicschool_pvalue = stats.ttest_ind(higher_publicschool, lower_publicschool)
        nonpublicschool_tscore, nonpublicschool_pvalue = stats.ttest_ind(higher_nonpublicschool, lower_nonpublicschool)
        
        r = [
            {
                "type": "num_hospital",
                "higher_income": avg(higher_hospital),
                "lower_income": avg(lower_hospital),
                "tscore": hospital_tscore,
                "pvalue": hospital_pvalue
            },
            {
                "type": "num_school",
                "higher_income": avg(higher_school),
                "lower_income": avg(lower_school),
                "tscore": school_tscore,
                "pvalue": school_pvalue
            },
            {
                "type": "num_publicschool",
                "higher_income": avg(higher_publicschool),
                "lower_income": avg(lower_publicschool),
                "tscore": publicschool_tscore,
                "pvalue": publicschool_pvalue
            },
            {
                "type": "num_nonpublicschool",
                "higher_income": avg(higher_nonpublicschool),
                "lower_income": avg(lower_nonpublicschool),
                "tscore": nonpublicschool_tscore,
                "pvalue": nonpublicschool_pvalue
            }
        ]
        repo['kobesay.income_infrastructure_ttest'].insert_many(r)
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

        this_script = doc.agent('alg:kobesay#do_ttest', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        income_infrastructure = doc.entity('dat:kobesay#income_infrastructure', {'prov:label':'region income and infrastructure', prov.model.PROV_TYPE:'ont:DataSet'})
        do_ttest = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime, {'prov:label':'T test on region income and infrastructure'})
        doc.wasAssociatedWith(do_ttest, this_script)

        income_infrastructure_ttest = doc.entity('dat:kobesay#income_infrastructure_ttest', {prov.model.PROV_LABEL:'Do T test on region income and infrastructure', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(income_infrastructure_ttest, this_script)
        doc.wasGeneratedBy(income_infrastructure_ttest, do_ttest, endTime)
        doc.wasDerivedFrom(income_infrastructure_ttest, income_infrastructure, do_ttest, do_ttest, do_ttest)

        repo.logout()
                  
        return doc

"""
# TEST
do_ttest.execute()
doc = do_ttest.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))
"""