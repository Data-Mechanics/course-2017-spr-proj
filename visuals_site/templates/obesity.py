import dml

client = dml.pymongo.MongoClient()
repo = client.repo
repo.authenticate('asafer_asambors_maxzm_vivyee','asafer_asambors_maxzm_vivyee')

obesity = repo['asafer_asambors_maxzm_vivyee.obesity']

geojson = open('obesity.js', 'w')
geojson.write('var obesity_json = \n')
geojson.write('{ "type": "FeatureCollection",'+"\n")
geojson.write('"features": ['+"\n")

for o in obesity.find():
    geojson.write('{ "type": "Feature",' + "\n")

    if 'data_value' in o:
        geojson.write('"properties":{"percentage":"' + o['data_value'] + '"')
    else:
        geojson.write('"properties":{"percentage":"0"')

    geojson.write(', "population_size":"' + o['population2010'] + '"},')
    geojson.write('"geometry": {"type": "Point", "coordinates": [')

    lat = o['geolocation']['latitude']
    lon = o['geolocation']['longitude']

    geojson.write(lon + ',' + lat + ']}},\n')

geojson.write(']}')
geojson.close()
print('Finished writing obesity.js')

