from cProfile import Profile
from config import *
import os
from src.dataloader import dataLoader
import pandas as pd

class db(object):
    """
    Create a mock db, use singleton pattern.
    Basic idea of implementation is sorting by name and use that index as primary key
    And create a hashmap which key is the pk, value is the column of data.
    This can be done to different column, use
    
    """

    @profile
    def __init__(self, path="./"):
        dl = dataLoader(path)
        dl.load()
        self.data = pd.DataFrame(dl.data)
        del dl
        

    def get(self):
        pass

    def delet(self):
        pass

    def desc(self):
        return self.data