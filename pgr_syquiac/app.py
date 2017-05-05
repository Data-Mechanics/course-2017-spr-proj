import flask
from flask import Flask, Response, request, render_template, url_for, send_from_directory

from correlation_checkups_app import correlation_checkups_app
import os

app = Flask(__name__)
app._static_folder = os.path.abspath("static")


@app.route('/', methods=['GET', 'POST'])
def getCorrelationsAll():
    if request.method == 'GET':
        #getcorrelation and pvalue (correlation, pvalue)
        coefficient_pvalue = correlation_checkups_app.execute(100)
        correlation_coefficient = coefficient_pvalue[0]
        pvalue = coefficient_pvalue[1]

        return render_template('main.html', allcorrelations = correlation_coefficient, pvalue = pvalue)
    else:
        distance = request.form.get('distance')
        if distance == 0: # Just get all the data points
            coefficient_pvalue = correlation_checkups_app.execute(100)
        else:
        	correlation_pvalue = correlation_checkups_app.execute(distance)
        
        correlation_coefficient = correlation_pvalue[0]
        pvalue = correlation_pvalue[1]
        return render_template('main.html', resutls = 'hello', onecorrelation = correlation_coefficient, pvalue = pvalue, distance = distance)


# @app.route('/static/css/filter.css', methods=['GET'])
# def getFile():
#     return Response(open('static/stylesheets/filter.css').read())

# @app.route('static/js/<path:path>')