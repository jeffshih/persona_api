import os
from os import path as osp
import fnmatch
import datetime as dt

def findFile(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(osp.join(root, name))
    return result

