from src.config import *
from flask_restful import Resource
from flask import request, jsonify
from src.database import database
from src.errorHandler import *

db = database()


class Search(Resource):
    def get(self, username):
        """
        If we are using a formal rdbms or we have orm, we can perform general query
        here only query for users
        """
        searchResult = db.search(username)
        if not searchResult :
            raise InvalidUsage.user_not_found()
        return template(searchResult, "Success", 200)
        
class SearchRange(Resource):
    """
    Implement pagination by passing parameters through url.
    If not passed, default page is 0 and pageSize is 1000
    """
    def get(self):
        res = {}
        try:
            page = int(request.args.get("page") if request.args.get("page") else 0)
            pageSize = int(request.args.get("pageSize") if request.args.get("pageSize") else 1000)
            start = pageSize*(page+1)
            end = start+pageSize
            if start >= end or page < 0 or pageSize <= 0:
                raise InvalidUsage.invalid_search_range()
            searchResult = db.searchRange(start,end)
            res["status"] = "Success"
            res["data"] = searchResult
        except ValueError as e:
            res["status"] = "Fail"
            res["data"] = "Invalid search range"
        finally:
            return jsonify(res)

class Delete(Resource):
    """
    Implement delete data by username
    """
    def delete(self,username):
        res = {}
        try:
            if not db.search(username):
                raise ValueError
            db.delete(username)
            res["status"] = "Success"
            res["data"] = "Delete {}".format(username)
        except ValueError as e:
            res["status"] = "Fail"
            res["data"] = "username {} does not exist".format(username)
        finally:
            return jsonify(res) 
