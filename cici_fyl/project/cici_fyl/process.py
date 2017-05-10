import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import method2
import scipy.stats
import csv
import geoleaflet

class process(dml.Algorithm):
    contributor = 'cici_fyl'
    reads = ['property','restaurant','school']
    writes = ['result']
    
    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('cici_fyl', 'cici_fyl')



        propertydata = repo['cici_fyl.property'].find()
        restaurantdata= repo['cici_fyl.restaurant'].find()
        schooldata= repo['cici_fyl.school'].find()

        #processing dataset. Select only the location of restaurants, school, and properties

        schooltemp= method2.project(schooldata,lambda t: t["geometry"]["coordinates"])
        schooltemp1= method2.project(schooltemp,lambda t: (t[0],t[1]))
        schoolcoordinates1= method2.select(schooltemp1, lambda t: abs(t[0])>0.0001 and abs(t[1])>0.0001)

        schoolcoordinates= method2.project(schoolcoordinates1,lambda t:(t[1],t[0]))

        propertytemp= method2.select(propertydata, lambda t: t["gross_tax"]!=0)
        propertytemp1= method2.project(propertytemp,lambda t: t["location"] if "location" in t else None)
        propertytemp2= method2.select(propertytemp1, lambda t: t!=None)
        propertytemp3= method2.project(propertytemp2,lambda t: method2.stringprocess(t))
        propertycoordinates= method2.select(propertytemp3, lambda t: abs(t[0])>0.0001 and abs(t[1])>0.0001)

       
 

        restauranttemp= method2.project(restaurantdata,lambda t: t["location"]["coordinates"])
        restauranttemp1= method2.project(restauranttemp,lambda t: (t[0],t[1]))
        restaurantcoordinates1= method2.select(restauranttemp1,lambda t: abs(t[0])>0.0001 and abs(t[1])>0.0001)

        restaurantcoordinates= method2.project(restaurantcoordinates1,lambda t:(t[1],t[0]))

        coordinates= method2.union(schoolcoordinates,restaurantcoordinates)

        mean= [(42.25246, -71.11896), (42.3466, -71.14185), (42.35201, -71.13770), (42.37527867719902, -71.03389058362008)]

        if trial:
            coordinates= coordinates[0:200]
        result= method2.kmeans(mean,coordinates)
        print(result)


        propertydistancetemp= method2.project(propertytemp,lambda t: {"id":t["_id"],"address":t["full_address"],"distance":0,"coordinates":t["location"],"tax":int(t["gross_tax"])})
        propertydistancetemp1= method2.project(propertydistancetemp,lambda t: method2.stringprocess1(t))

        propertydistancetemp2= method2.project(propertydistancetemp1,lambda t: method2.stringprocess2(t))
        print(propertydistancetemp2)

        propertycoor= method2.project(propertydistancetemp1,lambda t: [t["coordinates"][1],t["coordinates"][0],t["tax"]])
        propertydistance= method2.project(propertydistancetemp2,lambda t: method2.distance_to_mean(result,t))

        property_tax= method2.project(propertydistance,lambda t: t["tax"])
        property_distance= method2.project(propertydistance,lambda t: t["distance"])

        property_tax= method2.project(propertydistancetemp, lambda t: t["tax"])


        if trial:
            property_tax=property_tax[0:200]
            property_distance=property_distance[0:200]

        #calculate correlation and P-value 

        correlation = method2.corr(property_tax,property_distance)
        p= method2.p(property_tax,property_distance,trial)



        print(correlation)
        print(p)

        x= [{"kmeans":result,"correlation":correlation,"p-value":p}]

        repo.dropCollection("result")
        repo.createCollection("result")
        repo['cici_fyl.result'].insert_many(x)
    


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
        repo.authenticate('cici_fyl', 'cici_fyl')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        # doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')

        # doc.add_namespace('bod','http://bostonopendata-boston.opendata.arcgis.com/datasets/')

        this_script = doc.agent('alg:cici_fyl#process', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
       
        property_data = doc.entity('dat:cici_fyl#property', {prov.model.PROV_LABEL:'Boston property', prov.model.PROV_TYPE:'ont:DataSet'})
        school_data = doc.entity('dat:cici_fyl#school', {prov.model.PROV_LABEL:'Boston property', prov.model.PROV_TYPE:'ont:DataSet'})
        restaurant_data = doc.entity('dat:cici_fyl#restaurant', {prov.model.PROV_LABEL:'Boston property', prov.model.PROV_TYPE:'ont:DataSet'})
        result_data=doc.entity('dat:cici_fyl#result',  {prov.model.PROV_LABEL:'Boston property', prov.model.PROV_TYPE:'ont:DataSet'})

        mean = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        corr = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(corr, this_script)
        doc.wasAssociatedWith(mean, this_script)
        
        doc.usage(mean,property_data,startTime, None)
        doc.usage(mean,school_data,startTime, None)
        doc.usage(mean,restaurant_data,startTime, None)
        doc.usage(corr, property_data, startTime, None)

        doc.wasDerivedFrom(result_data, property_data, mean)
        doc.wasDerivedFrom(result_data, restaurant_data, mean)
        doc.wasDerivedFrom(result_data, school_data, mean)
        


        doc.wasAttributedTo(result_data, this_script)
          

        repo.logout()
                  
        return doc

process.execute()

