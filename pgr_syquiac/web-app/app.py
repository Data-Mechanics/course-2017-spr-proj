import flask
# import jsonschema
from flask import Flask, Response, jsonify, abort, make_response, request, render_template, send_from_directory, url_for
# from flask_httpauth import HTTPBasicAuth
# from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

from retrieveData import retrieveData
from transformation0 import transformation0
from correlation_checkups_app import correlation_checkups_app
import os

app = Flask(__name__)
app._static_folder = os.path.abspath("static")
#print(os.path.abspath(app._static_folder))

CORS(app)

@app.route('/', methods=['GET', 'POST'])
def getCorrelationsAll():
    if request.method == 'GET':
        #getcorrelation and pvalue (correlation, pvalue)
        coefficient_pvalue = correlation_checkups_app.execute(100)
        #doc = correlation_checkups_hospital.provenance()
        correlation_coefficient = coefficient_pvalue[0]
        pvalue = coefficient_pvalue[1]
        # print ("Stuff is happening!")
        #return page
        return render_template('main.html', allcorrelations = correlation_coefficient, pvalue = pvalue)
    else:
        distance = request.form.get('distance')
        if distance == 0: # Just get all the data points
            coefficient_pvalue = correlation_checkups_app.execute(100)
        else:
        	correlation_pvalue = correlation_checkups_app.execute(distance)
        # getCorrelation(distance)
        # print(distance)
        
        correlation_coefficient = correlation_pvalue[0]
        pvalue = correlation_pvalue[1]
        return render_template('main.html', resutls = 'hello', onecorrelation = correlation_coefficient, pvalue = pvalue, distance = distance)

