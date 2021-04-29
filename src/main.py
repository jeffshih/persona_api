import sys
import os
APP_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
sys.path.append(PROJECT_ROOT)
from src.config import *
from flask import Flask
from flask import jsonify
from flask import request
from flask_restful import Api
from src.controller import *


app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return 'Hello'

api.add_resource(Search,'/search/<string:username>')
api.add_resource(SearchRange,'/people')
api.add_resource(Delete, '/people/<string:username>')

if __name__ == '__main__':
    app.run()