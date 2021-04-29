from src.config import *
from src.dataloader import dataLoader


"""
In db I do not handle ValueError other exception,
I'll keep this module atomic, as close to the orm as possible.
Just like the domain layer.
"""


class database(object):
    """
    Create a mock db, basic idea of implementation is using a hashmap , 
    use username as key for O(1) search. But it's not extendable.

    If it comes to generalization, we can do a trade of for different implemenation.
    For example:
    Use read in sequence index as primary key and sort each column and keep the relative index.

    "username"
    [jeffshih, richard, erlich, bighead]
    [2 , 3, 1, 0]

    "name"
    ["Hsueh-Fu", "Richard Hendrick", "Erlich Bachman", "Nelson Bighetti"]
    [1, 3, 0, 2]

    by doing so we can do binary search for different column within O(logN)
    Python built in sort is tim sort, which is stable, so the duplicate value can be mapped to the origin array.
    """


    def __init__(self, path="./"):
        """
        Load in the data with dataLoader, create a hashtable and use username as key
        and the value is a list of json object(dict).
        Keep the raw data list for pagination
        """
        dl = dataLoader(path)
        dl.load()
        self.__data = {}
        self.__raw = dl.data
        self.__process(dl.data)

    def __process(self, raw_data):
        for origin_json in raw_data:
            username = origin_json["username"]
            if username in self.__data.keys():
                self.__data[username].append(origin_json)
            else:
                self.__data[username] = []


    def search(self,username):
        """
        search the hashtable and return the value
        """
        return self.__data.get(username)

    def delete(self,username):
        """
        If the user does not exist, return false,
        Else delete the element, which is all the profile with same username.
        """
        if self.__data.get(username) == None:
            return False
        else:
            del self.__data[username]
            return True

    def searchRange(self, start, end):
        """
        return the profile within certain range, computation of the pagination is done
        in the controller layer.
        """
        return self.__raw[start:end]