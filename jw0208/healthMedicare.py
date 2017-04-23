import urllib.request
import json
import dml
import prov.model
import datetime
import uuid



class healthMedicare(dml.Algorithm):
    contributor = 'jw0208'
    reads = ['jw0208.medicare', 'jw0208.health']
    writes = ['jw0208.healthMedicare']



    @staticmethod



    def execute(trial=False):
        startTime = datetime.datetime.now()

        def project(R, p):
            return [p(t) for t in R]

        def select(R, s):
            return [t for t in R if s(t)]

        def product(R, S):
            return [(t, u) for t in R for u in S]

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('jw0208', 'jw0208')



        medicare = repo['jw0208.medicare']
        health = repo['jw0208.health']

        health_array = []

        for document in health.find():
            health_array.append((document['locationabbr'], document['data_value']))

        # print (health_array);


        state = []

        for document in medicare.find():
            state.append((document['state'], document['score'], 1))
        #print(state)

        state_medicare_average = []
        keys = {r[0] for r in state}

        for key in keys:
            state_medicare_average.append((key, str(sum([float(v) for (k, v, s) in state if k == key]) / sum([s for (k, v, s) in state if k == key]))))

        medicare_array = []

        for i in state_medicare_average:
            medicare_array.append((i[0], i[1]))
        #print (medicare_array)

        x = project(select(product(medicare_array, health_array), lambda t: t[0][0] == t[1][0]), lambda t: (t[0][0], t[0][1], t[1][1]))



        y = []
        for i in range(0, 50):
            y.append({'state': x[i][0], 'medicare spent vs national level': x[i][1], 'annual physically&mentally unhealthydays': x[i][2]})

        #print (y)


        repo.dropPermanent('jw0208.healthMedicare')
        repo.createPermanent('jw0208.healthMedicare')
        repo['jw0208.healthMedicare'].insert_many(y)

        repo.logout()
        endTime = datetime.datetime.now()

        return {"start": startTime, "end": endTime}

    @staticmethod
    def provenance(doc=prov.model.ProvDocument(), startTime=None, endTime=None):
        '''
        Create the provenance document describing everything happening
        in this script. Each run of the script will generate a new
        document describing that invocation event.
        '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('jw0208', 'jw0208')

        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/')  # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/')  # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#')  # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/')  # The event log.
        doc.add_namespace('cdg', 'https://chronicdata.cdc.gov/resource/')

        this_script = doc.agent('alg:jw0208#healthMedicare',
                                {prov.model.PROV_TYPE: prov.model.PROV['SoftwareAgent'], 'ont:Extension': 'py'})
        resource = doc.entity('cdg:fq5d-abxc',{'prov:label': 'State physically and mentally unhealthy days vs. state medicare spent on patient compare to national level',
                               prov.model.PROV_TYPE: 'ont:DataResource', 'ont:Extension': 'json'})
        this_healthMedicare = doc.activity('log:uuid' + str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(this_healthMedicare, this_script)
        doc.usage(this_healthMedicare, resource, startTime, None,{prov.model.PROV_TYPE: 'ont:Retrieval'})

        healthMedicare = doc.entity('dat:jw0208#healthMedicare', {prov.model.PROV_LABEL:'State physically and mentally unhealthy days vs. state medicare spent on patient compare to national level', prov.model.PROV_TYPE:'ont:DataSet'})
        health = doc.entity('dat:jw0208#health', {prov.model.PROV_LABEL:'State physically and mentally unhealthy days in year 2015', prov.model.PROV_TYPE:'ont:DataSet'})
        medicare = doc.entity('dat:jw0208#medicare', {prov.model.PROV_LABEL:'state hospital medicare spent on each patient compare to national level in year 2015', prov.model.PROV_TYPE:'ont:DataSet'})

        doc.wasAttributedTo(healthMedicare, this_script)
        doc.wasGeneratedBy(healthMedicare, this_healthMedicare, endTime)
        doc.wasDerivedFrom(health, resource, this_healthMedicare, this_healthMedicare, this_healthMedicare)
        doc.wasDerivedFrom(medicare, resource, this_healthMedicare, this_healthMedicare, this_healthMedicare)

        #repo.record(doc.serialize())  # Record the provenance document.
        repo.logout()

        return doc


#healthMedicare.execute()
# doc = healthMedicare.provenance()
# # print(doc.get_provn())
# # print(json.dumps(json.loads(doc.serialize()), indent=4))
