from flask.json import jsonify
from flask.wrappers import Response
from src.util import *


def template(data, status, code=500):
    return {"data":data, "status":status, "status_code":code}

USER_NOT_FOUND = template(["username not found"], "Fail", 404)
UNKNOWN_ERROR = template([],"Fail",500)
INVALIDE_SEARCH_RANGE = template(["Invalid search range"], "Fail", 404)
UNKNOWN_ENDPOINT = template(["Endpoint does not exist"], "Fail", 404)
INVALID_REQUEST = template(["Invalid request method"], "Fail", 405)

class InvalidUsage(Exception):
    status_code = 500
    def __init__(self, data, status, status_code):
        Exception.__init__(self)
        self.data = data
        self.status = status
        if status_code is not None:
            self.status_code = status_code
        self.response = template(data, status, status_code)

    def to_json(self):
        return jsonify(self.response)

    @classmethod
    def user_not_found(cls):
        return cls(**USER_NOT_FOUND)

    @classmethod
    def unknown_error(cls):
        return cls(**UNKNOWN_ERROR)

    @classmethod
    def invalid_search_range(cls):
        return cls(**INVALIDE_SEARCH_RANGE)

    @classmethod
    def unknown_endpoint(cls):
        return cls(**UNKNOWN_ENDPOINT)
