'''
    Pauline Ramirez and Carlos Syquia
    transformation0.py
    Combining the open spaces datasets between Boston and Cambridge, obesity rates and how far people are from open spaces
'''

import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import sodapy


class transformation0(dml.algorithm):
    contributor = 'pgr_syquiac'
    reads = ['pgr_syquiac.camopenspaces', 'pgr_syquiac.bosopenspaces', 'pgr_syquia.cdc']

    @staticmethod
    def execute(trial = False):
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('pgr_syquiac', 'pgr_syquiac', 'pgr_syquiac')

        #start
        camopenspacesRepo = repo.pgr_syquiac.camopenspaces
        bosopenspacesRepo = repo.pgr_syquiac.bosopenspaces
        cdcRepo = repo.pgr_syquiac.cdc

        #get boston open spaces

        #get cambridge open spaces, location

        #



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
            repo.authenticate('pgr_syquiac', 'pgr_syquiac')
            doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
            doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
            doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
            doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
            doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')
            doc.add_namespace('cdc', 'https://chronicdata.cdc.gov/resource/')
            doc.add_namespace('cdp', 'https://data.cambridgema.gov/resource/')

            this_script = doc.agent('alg:pgr_syquiac#retrieveData', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
