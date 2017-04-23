# assignBusYards.py

import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import math
import random
from geopy.distance import vincenty

class assignBusYards(dml.Algorithm):
    contributor = 'echogu_wei0496_wuhaoyu'
    reads = ['echogu_wei0496_wuhaoyu.pickup_sequence', 'echogu_wei0496_wuhaoyu.buses']
    writes = ['echogu_wei0496_wuhaoyu.bus_route']

    @staticmethod
    def execute(trial = False):
        ''' find the closest bus yard
        '''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('echogu_wei0496_wuhaoyu', 'echogu_wei0496_wuhaoyu')

        # loads the collection
        raw_pickup_sequence = repo['echogu_wei0496_wuhaoyu.pickup_sequence'].find()
        pickup_sequence = []
        for item in raw_pickup_sequence:
            pickup_sequence.append({'mean': item['mean'],
                                    'school': item['school'],
                                    'location': item['location'],
                                    'pickup_sequence': item['pickup_sequence']})

        # Trial mode
        if trial:
            if len(pickup_sequence) == 1:
                pass
            else:
                pickup_sequence = random.choices(pickup_sequence, k = 1)

        # loads the bus yard information
        raw_buses = repo['echogu_wei0496_wuhaoyu.buses'].find()
        buses = []
        for item in raw_buses:
            buses.append({'coordinates': tuple(reversed(item['geometry']["coordinates"])),
                          'yard': item['properties']['yard'],
                          'address': item['properties']['address']})

        # find the closest bus yard to the first or last student in sequence
        route = []
        for s in pickup_sequence:
            origin = []
            min_dis = float('inf')
            first_student = s['pickup_sequence'][0]
            first_student_loc = (first_student['latitude'], first_student['longitude'])

            for bus in buses:
                temp_dis = assignBusYards.distance(bus['coordinates'], first_student_loc)
                if(temp_dis < min_dis):
                    origin = bus
                    min_dis = temp_dis
            route.append({'school': s['school'],
                          'school location': s['location'],
                          'bus yard': origin['yard'],
                          'yard location': origin['coordinates'],
                          'yard address': origin['address'],
                          'pickup_sequence': s['pickup_sequence']})

        # store bus routes into the database
        repo.dropCollection('bus_route')
        repo.createCollection('bus_route')
        repo['echogu_wei0496_wuhaoyu.bus_route'].insert_many(route)
        repo['echogu_wei0496_wuhaoyu.bus_route'].metadata({'complete': True})
        print(repo['echogu_wei0496_wuhaoyu.bus_route'].metadata(), "Saved Bus Route")

        endTime = datetime.datetime.now()

        return {"start": startTime, "end": endTime}

    @staticmethod
    def provenance(doc=prov.model.ProvDocument(), startTime=None, endTime=None):
        ''' Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
        '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('echogu_wei0496_wuhaoyu', 'echogu_wei0496_wuhaoyu')

        # create document object and define namespaces
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/')  # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/')  # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#')  # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/')  # The event log.

        # define entity to represent resources
        this_script = doc.agent('alg:echogu_wei0496_wuhaoyu#assignBusYards', {prov.model.PROV_TYPE: prov.model.PROV['SoftwareAgent'], 'ont:Extension': 'py'})
        resource_pickup_sequence = doc.entity('dat:echogu_wei0496_wuhaoyu#pickup_sequence', {'prov:label': 'pickup_sequence', prov.model.PROV_TYPE: 'ont:DataSet'})
        resource_buses = doc.entity('dat:echogu_wei0496_wuhaoyu#buses', {'prov:label': 'buses', prov.model.PROV_TYPE: 'ont:DataSet'})

        # # define activity to represent invocaton of the script
        run_assignBusYards = doc.activity('log:uuid' + str(uuid.uuid4()), startTime, endTime)
        # associate the activity with the script
        doc.wasAssociatedWith(run_assignBusYards, this_script)
        # indicate that an activity used the entity
        doc.usage(run_assignBusYards, resource_pickup_sequence, startTime, None, {prov.model.PROV_TYPE: 'ont:Computation'})
        doc.usage(run_assignBusYards, resource_buses, startTime, None, {prov.model.PROV_TYPE: 'ont:Computation'})

        # for the data obtained, indicate that the entity was attributed to what agent, was generated by which activity and was derived from what entity
        bus_route = doc.entity('dat:echogu_wei0496_wuhaoyu#bus_route', {prov.model.PROV_LABEL: 'bus_route', prov.model.PROV_TYPE: 'ont:DataSet'})
        doc.wasAttributedTo(bus_route, this_script)
        doc.wasGeneratedBy(bus_route, run_assignBusYards, endTime)
        doc.wasDerivedFrom(bus_route, resource_pickup_sequence, run_assignBusYards, run_assignBusYards, run_assignBusYards)
        doc.wasDerivedFrom(bus_route, resource_buses, run_assignBusYards, run_assignBusYards, run_assignBusYards)

        repo.logout()

        return doc

    @staticmethod
    def distance(point1, point2):
        return vincenty(point1, point2).miles

# assignBusYards.execute()
# doc = assignBusYards.provenance()
# print(doc.get_provn())
# print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof
