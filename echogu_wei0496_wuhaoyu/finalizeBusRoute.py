# optimizeBusRoute.py

import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import math
import random
import geojson
import re
#import xlsxwriter

class finalizBusRoute(dml.Algorithm):
    contributor = 'echogu_wei0496_wuhaoyu'
    reads = ['echogu_wei0496_wuhaoyu.bus_route']
    writes = ['echogu_wei0496_wuhaoyu.bus_route_final']

    @staticmethod
    def execute(trial = False):
        ''' finalize bus routes and convert to geojson format
        '''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('echogu_wei0496_wuhaoyu', 'echogu_wei0496_wuhaoyu')

        # loads the collection
        bus_route = repo['echogu_wei0496_wuhaoyu.bus_route'].find()
        schools = repo['echogu_wei0496_wuhaoyu.schools'].find()

        # convert to geojson
        features = []
        features_routes = []    # collection of routes
        features_schools = []   # collection of schools
        features_yards = []     # collection of yards
        schools = []            # handle duplicates
        yards = []              # handle duplicates
        count = 1

        for r in bus_route:
            features_one_school = []

            # extract properties
            colors = "0123456"
            random_color = ''.join(random.choices(colors, k = 6))
            properties = {'school': r['school'],
                                 'yard': r['bus yard'],
                                 'stroke': '#' + random_color,
                                 'stroke-width': 1,
                                 'stroke-opacity': 0.3}
            properties_one_school = {'school': r['school'],
                                     'yard': r['bus yard'],
                                     'stroke': '#003534',
                                     'stroke-width': 2}

            # extract routes info: yard -> student -> school
            sequence = r['pickup_sequence']
            route = []
            yard = tuple(reversed(r['yard location']))
            route += [yard]
            for s in sequence:
                s = tuple((s['longitude'], s['latitude']))
                route += [s]
            school = tuple(reversed(r['school location']))
            route += [school]
            geometry = geojson.LineString(route)

            # save routes
            filename = r['school']
            filename = re.sub('[ ?.!/;:]', '', filename)
            features_one_school.append(geojson.Feature(geometry=geometry, properties=properties_one_school))      # graph for each school
            features_routes.append(geojson.Feature(geometry=geometry, properties=properties))    # graph with routes only
            features.append(geojson.Feature(geometry=geometry, properties=properties))                  # graph with routes, schools and yards

            # extract school info
            properties_schools = {'school': r['school'],
                                  'marker-size': 'small',
                                  'marker-symbol': 'college',
                                  'marker-color': '#8cbdbc'}
            features_one_school.append(geojson.Feature(geometry=geojson.Point(tuple(reversed(r['school location']))), properties=properties_schools))

            # extract yard info
            properties_yards = {'yard': r['bus yard'],
                                'address': r['yard address'],
                                'marker-size': 'small',
                                'marker-symbol': 'bus',
                                'marker-color': '#d8b0e2'}
            features_one_school.append(geojson.Feature(geometry=geojson.Point(tuple(reversed(r['yard location']))), properties=properties_yards))

            # handle duplicate schools and yards
            if r['school'] not in schools:
                features_schools.append(geojson.Feature(geometry=geojson.Point(tuple(reversed(r['school location']))), properties=properties_schools))
                schools += [r['school']]
            if r['bus yard'] not in yards:
                features_yards.append(geojson.Feature(geometry=geojson.Point(tuple(reversed(r['yard location']))), properties=properties_yards))
                yards += [r['bus yard']]

            open('echogu_wei0496_wuhaoyu/visualizations/geojson/' + "%03d" % count + filename + '.geojson', 'w').write(geojson.dumps(geojson.FeatureCollection(features_one_school), indent=2))
            count += 1
            # end of for

        features += features_schools
        features += features_yards

        open('echogu_wei0496_wuhaoyu/visualizations/geojson/bus_route.geojson', 'w').write(geojson.dumps(geojson.FeatureCollection(features_routes), indent=2))
        open('echogu_wei0496_wuhaoyu/visualizations/geojson/bus_route_schools.geojson', 'w').write(geojson.dumps(geojson.FeatureCollection(features), indent=2))

        # store bus route into database in geojson format
        repo.dropCollection('bus_route_final')
        repo.createCollection('bus_route_final')
        repo['echogu_wei0496_wuhaoyu.bus_route_final'].insert_many(features_routes)
        repo['echogu_wei0496_wuhaoyu.bus_route_final'].metadata({'complete': True})
        print(repo['echogu_wei0496_wuhaoyu.bus_route_final'].metadata(), "Saved Bus Route Final")

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
        this_script = doc.agent('alg:echogu_wei0496_wuhaoyu#finalizeBusRoute', {prov.model.PROV_TYPE: prov.model.PROV['SoftwareAgent'], 'ont:Extension': 'py'})
        resource_bus_route = doc.entity('dat:echogu_wei0496_wuhaoyu#bus_route', {'prov:label': 'bus_route', prov.model.PROV_TYPE: 'ont:DataSet'})

        # define activity to represent invocaton of the script
        run_finalizeBusRoute = doc.activity('log:uuid' + str(uuid.uuid4()), startTime, endTime)
        # associate the activity with the script
        doc.wasAssociatedWith(run_finalizeBusRoute, this_script)
        # indicate that an activity used the entity
        doc.usage(run_finalizeBusRoute, resource_bus_route, startTime, None, {prov.model.PROV_TYPE: 'ont:Computation'})

        # for the data obtained, indicate that the entity was attributed to what agent, was generated by which activity and was derived from what entity
        bus_route_final = doc.entity('dat:echogu_wei0496_wuhaoyu#bus_route_final', {prov.model.PROV_LABEL: 'bus_route_final', prov.model.PROV_TYPE: 'ont:DataSet'})
        doc.wasAttributedTo(bus_route_final, this_script)
        doc.wasGeneratedBy(bus_route_final, run_finalizeBusRoute, endTime)
        doc.wasDerivedFrom(bus_route_final, resource_bus_route, run_finalizeBusRoute, run_finalizeBusRoute, run_finalizeBusRoute)

        repo.logout()

        return doc

finalizBusRoute.execute()
# doc = finalizeBusRoute.provenance()
# print(doc.get_provn())
# print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof
