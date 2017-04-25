from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import optimization_algorithm
import json

app = Flask(__name__)

info=None
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
@app.route("/")
def index():
    return render_template('index.html')

def send_file(path):
    return send_from_directory('/', path)

@app.route("/optimize/", methods=["GET"])
def optimize():
    return render_template('optimize.html')

@app.route("/optimize-result/", methods=["GET"])

def optimize_result():

    food=request.args["Food"]
    transport=request.args['Transport']
    safe=request.args['Safety']
    rent=request.args['Rent']
    # print(food,transport,safe,rent)
    result=optimization_algorithm.get_result(int(food),int(transport),int(safe),int(rent))
    res=result[:5]
    for i in res:
        i['grade']=[i['grade']['food'],i['grade']['transport'],i['grade']['safety'],i['grade']['rent']]
    global info
    info=res
    data = []
    for item in res:
        temp = {}
        temp['area'] = item['area']
        temp['postal_code'] = item['postal_code']
        temp['grade'] = item['grade']
        data.append(temp)
    return render_template('optimize-result.html',f=food,t=transport,s=safe,r=rent,res=res, data=data)

@app.route("/map/")
def get_map():
    global info
    # for dic in info:
    #     dic.pop('_id', None)
    return render_template('map.html',a=info[0],b=info[1],c=info[2],d=info[3],e=info[4])


@app.route("/static-analysis/")
def static_analysis():
    return render_template('static-analysis.html')

@app.route("/crimePercentage/")
def crimePercentage():
    return render_template('crimePercentage.html')

if __name__ == '__main__':
    app.run(debug=True)