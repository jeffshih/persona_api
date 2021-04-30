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
        page = int(request.args.get("page") if request.args.get("page") else 0)
        pageSize = int(request.args.get("pageSize") if request.args.get("pageSize") else 1000)
        start = pageSize*page
        end = start+pageSize
        if start >= end or page < 0 or pageSize <= 0:
            raise InvalidUsage.invalid_search_range()
        searchResult = db.searchRange(start,end)
        return template(searchResult, "Success", 200)

class Delete(Resource):
    """
    Implement delete data by username
    """
    def delete(self,username):
        if not db.search(username):
            raise InvalidUsage.user_not_found()
        db.delete(username)
        data = "Delete {}".format(username)
        return template(data, "Success", 200)