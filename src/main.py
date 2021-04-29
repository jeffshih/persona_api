import sys
import os
APP_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
sys.path.append(PROJECT_ROOT)
from src.config import *
from flask import Flask, jsonify, request
from flask_restful import Api
from src.views import *


app = Flask(__name__)

def errorhandler(error):
    response = error.to_json()
    return response

#app.errorhandler(InvalidUsage)(errorhandler)


api = Api(app)

@app.route('/')
def index():
    return 'Hello'


@app.errorhandler(404)
def not_found_error(error):
    raise InvalidUsage.unknown_endpoint()

api.add_resource(Search,'/search/<string:username>')
api.add_resource(SearchRange,'/people')
api.add_resource(Delete, '/people/<string:username>')


if __name__ == '__main__':
    app.run()