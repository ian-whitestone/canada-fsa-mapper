from app import app
from flask import render_template

from app import PostalLoader

from flask import flash, Blueprint, request, redirect, render_template, url_for
from flask import jsonify, Markup, send_from_directory, Response, make_response
from flask.views import MethodView
import json
import os
import requests

# BG_data = Blueprint('BG_data', __name__, template_folder='templates')
# ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/fsa_api')
def fsa_api():
    minlat = request.args.get('minlat')
    minlng = request.args.get('minlng')
    maxlat = request.args.get('maxlat')
    maxlng = request.args.get('maxlng')

    canada_fsa_list = PostalLoader.getCanadaFSA() ## sample polygon

    fsa_list = []

    for geom in canada_fsa_list:
        fsa = dict(geometry=geom, type='Feature')
        fsa['properties'] = dict(prop1=1,colour=4)
        fsa_list.append(fsa)

    response = jsonify(type='FeatureCollection', features=fsa_list)
    return response
