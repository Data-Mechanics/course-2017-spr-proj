import json
from flask import Flask, Response, request, render_template, redirect, url_for
import flask.ext.login as flask_lo

app = Flask(__name__)


# Home Page
@app.route('/', methods=['GET'])
def home():
	return render_template('index.html')


# Interactive Scatter Plot
