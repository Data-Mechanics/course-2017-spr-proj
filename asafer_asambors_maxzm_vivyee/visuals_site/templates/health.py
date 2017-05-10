import dml

client = dml.pymongo.MongoClient()
repo = client.repo
repo.authenticate('asafer_asambors_maxzm_vivyee','asafer_asambors_maxzm_vivyee')

health = repo['asafer_asambors_maxzm_vivyee.healthy_locations']

geojson = open('health.js', 'w')
geojson.write('var health_json = \n')
geojson.write('{ "location_type": "FeatureCollection",'+"\n")
geojson.write('"features": ['+"\n")

for h in health.find():
    geojson.write('{ "type": "Feature",' + "\n")
    geojson.write('"properties":{"type":"' + h['type'] + '"},')
    geojson.write('"geometry": {"type": "Point", "coordinates": [')

    lat = str(h['location'][1])
    lon = str(h['location'][0])

    geojson.write(lon + ',' + lat + ']}},\n')

geojson.write(']}')
geojson.close()
print('Finished writing health.js')

