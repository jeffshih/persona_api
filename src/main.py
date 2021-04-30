import sys
import os
APP_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
sys.path.append(PROJECT_ROOT)
from src.config import *
from flask import Flask
from flask_restful import Api
from src.views import *
from flasgger import Swagger


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config['SWAGGER'] = {'title':'Persona api', 'uiversion':2}
    swag = Swagger(app)

    """
    Handle all the unimplemented api.
    """
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify(InvalidUsage.unknown_endpoint().data), 404

    api = Api(app)
    api.add_resource(Search,'/search/<string:username>')
    api.add_resource(SearchRange,'/people')
    api.add_resource(Delete, '/people/<string:username>')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()