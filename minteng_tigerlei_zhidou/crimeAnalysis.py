import dml, prov.model
import datetime, uuid
import numpy as np
from scipy import stats
import warnings, os

class crimeAnalysis(dml.Algorithm):
    contributor = 'minteng_tigerlei_zhidou'
    reads = ['minteng_tigerlei_zhidou.crime', 'minteng_tigerlei_zhidou.box_count']
    writes = ['minteng_tigerlei_zhidou.statsresult', 'minteng_tigerlei_zhidou.crimeCount']
    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets.'''
        startTime = datetime.datetime.now()
        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('minteng_tigerlei_zhidou', 'minteng_tigerlei_zhidou')

        # every entry is one year, and inside the year, there will be 
        # the number of crime
        districtNum = repo['minteng_tigerlei_zhidou.box_count'].count()
        crimeVector = np.zeros([districtNum, 4, 12])
        crimeCount = []
        monthlyCount = np.zeros(48)


        for data in repo['minteng_tigerlei_zhidou.box_count'].find():
            crimeBox = {'_id': data['_id'], 'box': data['box'], 'area': data['area'], 'crimeNum': np.zeros(48, np.int)}
            # count crime from 2013 to 2017 48 month
            area = repo['minteng_tigerlei_zhidou.crime'].find({'location':{'$geoWithin':{ '$box': data['box']}}})
            for event in area:
                if event['year'] in [2012, 2017]: continue
                crimeVector[data['_id'] - 1][event['year'] - 2013][event['month'] - 1] += 1
                monthlyCount[(event['year'] - 2013) * 12 + (event['month'] - 1)] += 1
                crimeBox['crimeNum'][(event['year'] - 2013) * 12 + (event['month'] - 1)] += 1
            crimeBox['crimeNum'] = crimeBox['crimeNum'].tolist()
            crimeCount.append(crimeBox)

        for crimeBox in crimeCount:
            crimeBox['crimeRatio'] = np.zeros(48)
            for i in range(48):
                crimeBox['crimeRatio'][i] = crimeBox['crimeNum'][i] / monthlyCount[i]

            crimeBox['crimeRatio'] = crimeBox['crimeRatio'].tolist()



        # compute the correlation coefficient and p-value
        # of same district but different year
        warnings.filterwarnings("ignore")
        corrfP = [ [stats.pearsonr(crimeVector[k][i], crimeVector[k][i + 1]) for i in range(3)] for k in range(districtNum) ]

        # print("                    corrf             p-value      ")
        # for i in range(5):
        #     for block, dnum in zip(corrfP[i], range(districtNum)):
        #         print(str(i + 12) + ' - block {}:  '.format(dnum) + str(block[0]) + "   " + str(block[1]))
        
        ret = []
        pattern = dict(_id = 0, value = 0)
        for i in range(districtNum):
            tempDict = dict(pattern)
            tempDict['_id'] = i + 1
            tempDict['value'] = [ {'year': str(2013 + j) + '-' + str(2013 + j + 1), 
                                    'corcof': corrfP[i][j][0] if corrfP[i][j][0] != None else 0,
                                    'p': corrfP[i][j][1]} for j in range(3) ]
            ret.append(tempDict)
        
        current_dir = os.getcwd()
        # Create datadir if does not exist
        print(current_dir)
        if not os.path.exists(os.path.join(current_dir, 'minteng_tigerlei_zhidou/web/static/corAndP.csv')):
            with open(os.path.join(current_dir, 'minteng_tigerlei_zhidou/web/static/corAndP.csv'), 'w') as f:
                f.write('area,periodyear,avgemp,changeemp\n')
                for i in range(districtNum):
                    for j in range(3):
                        f.write(str(i + 1) + ',' + str(2013 + j) + ',' + 
                                str(abs(corrfP[i][j][0]) if not np.isnan(corrfP[i][j][0]) else 0) + ',' + 
                                str(corrfP[i][j][1]) + '\n')
                        f.flush()




        repo.dropCollection("statsresult")
        repo.createCollection("statsresult")
        repo['minteng_tigerlei_zhidou.statsresult'].insert_many(ret)

        repo.dropCollection("crimeCount")
        repo.createCollection("crimeCount")
        repo['minteng_tigerlei_zhidou.crimeCount'].insert_many(crimeCount)

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
        repo.authenticate('minteng_tigerlei_zhidou', 'minteng_tigerlei_zhidou')

        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.

        
        this_script = doc.agent('alg:minteng_tigerlei_zhidou#statsresult', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        
        statsresult_resource = doc.entity('dat:minteng_tigerlei_zhidou#box_count', {'prov:label':'box count and grade', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        statsresult_resource2 = doc.entity('dat:minteng_tigerlei_zhidou#crime', {'prov:label':'crime dataset', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        
        statsresult_result = doc.entity('dat:minteng_tigerlei_zhidou#statsresult', {prov.model.PROV_LABEL:'statistics result', prov.model.PROV_TYPE:'ont:DataSet'})
        crimeCount = doc.entity('dat:minteng_tigerlei_zhidou#crimeCount', {prov.model.PROV_LABEL:'crime Count', prov.model.PROV_TYPE:'ont:DataSet'})
        
        

        get_statsresult = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        
        doc.wasAssociatedWith(get_statsresult, this_script)
        doc.usage(get_statsresult, statsresult_resource,startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'})
        doc.usage(get_statsresult, statsresult_resource2,startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'})

        doc.wasAttributedTo(statsresult_result, this_script)
        doc.wasGeneratedBy(statsresult_result, get_statsresult, endTime)
        doc.wasDerivedFrom(statsresult_result, statsresult_resource, get_statsresult, get_statsresult, get_statsresult)
        doc.wasDerivedFrom(statsresult_result, statsresult_resource2, get_statsresult, get_statsresult, get_statsresult)

        
        get_crimeCount = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        
        doc.wasAssociatedWith(get_crimeCount, this_script)
        doc.usage(get_crimeCount, statsresult_resource,startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'})
        doc.usage(get_crimeCount, statsresult_resource2,startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'})

        doc.wasAttributedTo(crimeCount, this_script)
        doc.wasGeneratedBy(crimeCount, get_crimeCount, endTime)
        doc.wasDerivedFrom(crimeCount, statsresult_resource, get_crimeCount, get_crimeCount, get_crimeCount)
        doc.wasDerivedFrom(crimeCount, statsresult_resource2, get_crimeCount, get_crimeCount, get_crimeCount)

        
        
        repo.logout()
        return doc

# crimeAnalysis.execute()