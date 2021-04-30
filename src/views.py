from src.config import *
from flask_restful import Resource
from flask import request, jsonify
from src.database import database
from src.errorHandler import *

db = database()


class Search(Resource):
    """
        If we are using a formal rdbms or we have orm, we can perform general query
        here only query for users
    """
       
    def get(self, username):
        """
        Endpoint returning the searching result by username
        ---
        tags:
            - restful
        parameters:
            - in: path
              name: username
              required: true
              description: username of the target person
              type: string
        responses:
            200:
              description: Get the profile of the user
              examples:
                {"data": [{"job": "Retail manager", "company": "Jenkins LLC", "ssn": "ZZ 605364 T", "residence": "89 Angela street\nNew Marieview\nOX72 6TF", "current_location": [-74.8506105, 157.862558], "blood_group": "B-", "website": ["http://www.forster.info/"], "username": "twong", "name": "Roger Allen-Benson", "sex": "F", "address": "Flat 59i\nWood orchard\nNew Rachelville\nB7 9YZ", "mail": "cameron61@gmail.com", "birthdate": "1973-01-02"}], "status": "Success", "status_code": 200}
        """
        searchResult = db.search(username)
        if not searchResult :
            raise InvalidUsage.user_not_found()
        return template(searchResult, "Success", 200)
        
class SearchRange(Resource):
    """
    Implement pagination by passing parameters through url
    If not passed, default page is 0 and pageSize is 1000
    """
    def get(self):
        """
        Endpoint returning the result of all profile with pagination
        Default page is 0 and pageSize is 10000
        ---
        tags:
            - restful
        parameters:
            - in: query
              name: page
              required: false
              description: target page
              type: integer
            - in: query
              name: pageSize
              required: false
              description: number of rows to show per page
              type: integer
        responses:
            200:
              description: Get the profile of the user using page=1&pageSize=0
              examples:
                {"data": [{"job": "Retail manager", "company": "Jenkins LLC", "ssn": "ZZ 605364 T", "residence": "89 Angela street\nNew Marieview\nOX72 6TF", "current_location": [-74.8506105, 157.862558], "blood_group": "B-", "website": ["http://www.forster.info/"], "username": "twong", "name": "Roger Allen-Benson", "sex": "F", "address": "Flat 59i\nWood orchard\nNew Rachelville\nB7 9YZ", "mail": "cameron61@gmail.com", "birthdate": "1973-01-02"}], "status": "Success", "status_code": 200}
        """ 
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
        """
        Endpoint lets you delete the profile by username
        ---
        tags:
          - restful
        parameters:
          - in: path
            name: username
            required: true
            description: The username you want to delete
            type: string
        responses:
          200:
            description: Task deleted
            examples:
                {"data": "Delete louis87", "status": "Success", "status_code": 200}
        """
        if not db.search(username):
            raise InvalidUsage.user_not_found()
        db.delete(username)
        data = "Delete {}".format(username)
        return template(data, "Success", 200)