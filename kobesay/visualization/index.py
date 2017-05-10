from bson import json_util as jsonb
import pymongo
from flask import Flask, jsonify, abort, make_response, request, render_template, send_file

app = Flask(__name__, static_url_path='')

conn = pymongo.MongoClient('localhost',27017)
repo = conn.repo

# api for fetching raw data
@app.route('/app/api/v1/raw/hospital', methods=['GET'])
def get_raw_hospital():
    repo.authenticate('demo', 'demo')
    return jsonb.dumps(list(repo.demo.hospital.find()))

@app.route('/app/api/v1/raw/school/nonpublic', methods=['GET'])
def get_raw_school_nonpublic():
    repo.authenticate('demo', 'demo')
    return jsonb.dumps(list(repo.demo.nonpublicschool.find()))

@app.route('/app/api/v1/raw/school/public', methods=['GET'])
def get_raw_school_public():
    repo.authenticate('demo', 'demo')
    return jsonb.dumps(list(repo.demo.publicschool.find()))

@app.route('/app/api/v1/raw/income/2013', methods=['GET'])
def get_raw_income_2013():
    repo.authenticate('demo', 'demo')
    return jsonb.dumps(list(repo.demo.income2013.find()))

@app.route('/app/api/v1/raw/income/2014', methods=['GET'])
def get_raw_income_2014():
    repo.authenticate('demo', 'demo')
    return jsonb.dumps(list(repo.demo.income2014.find()))


# api for fetching region based data
@app.route('/app/api/v1/region/hospital', methods=['GET'])
def get_region_hospital():
    repo.authenticate('demo', 'demo')
    return jsonb.dumps(list(repo.demo.regionhospital.find()))

@app.route('/app/api/v1/region/school/nonpublic', methods=['GET'])
def get_region_school_nonpublic():
    repo.authenticate('demo', 'demo')
    return jsonb.dumps(list(repo.demo.regionnonpublicschool.find()))

@app.route('/app/api/v1/region/school/public', methods=['GET'])
def get_region_school_public():
    repo.authenticate('demo', 'demo')
    return jsonb.dumps(list(repo.demo.regionpublicschool.find()))

@app.route('/app/api/v1/region/school/all', methods=['GET'])
def get_region_school_all():
    repo.authenticate('demo', 'demo')
    return jsonb.dumps(list(repo.demo.regionschool.find()))

@app.route('/app/api/v1/region/income', methods=['GET'])
def get_region_income():
    repo.authenticate('demo', 'demo')
    return jsonb.dumps(list(repo.demo.regionincome.find()))


# api for fetching result data
@app.route('/app/api/v1/result/income_infra', methods=['GET'])
def get_result_income_infra():
    repo.authenticate('demo', 'demo')
    return jsonb.dumps(list(repo.demo.income_infrastructure.find()))


# api for analysis on result data
@app.route('/app/api/v1/analysis/pearsonr', methods=['GET'])
def get_analysis_pearsonr():
    repo.authenticate('demo', 'demo')
    return jsonb.dumps(list(repo.demo.income_infrastructure_pearsonr.find()))

@app.route('/app/api/v1/analysis/ttest', methods=['GET'])
def get_analysis_ttest():
    repo.authenticate('demo', 'demo')
    return jsonb.dumps(list(repo.demo.income_infrastructure_ttest.find()))


# visualization web response
@app.route('/app/visual/region', methods=['GET'])
def visualize_region():
    return send_file('./region.html')

@app.route('/app/visual/analysis', methods=['GET'])
def visualize_analysis():
    return send_file('./analysis.html')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'nothing here'}), 404)


if __name__ == '__main__':
    app.run(debug=True)