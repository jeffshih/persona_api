import sys 
sys.path.append("./")
import os
import json
from zipfile import ZipFile
from src.util import *
from fnmatch import fnmatch
import datetime as dt

# Creating a mock db using fake_profile.zip this will unzip the file.
# Load in the json file, here we can use a decorator pattern for different source of storage
# We can implement different loading method due to different flat file type.
# For json we need to load the whole file in, but for csv we can separate by batch.
# These behavior depends on the flat file.

class loader():
    """
    Base component for the flat file loader
    
    """

    def decompress(self):
        pass 

    def load(self):
        pass


class compressDecorator(loader):

    __loader: loader = None 
    
    def __init__(self, loader:loader):
        self.__loader = loader

    @property
    def loader(self):
        return self.__loader
    
    def decompress(self):
        return self.__loader.decompress()

class loadDecorator(loader):
    
    __loader: loader = None 
    
    def __init__(self, loader:loader):
        self.__loader = loader

    @property
    def loader(self):
        return self.__loader
    
    def load(self):
        return self.__loader.load()
    

class zipDecompressor(compressDecorator):

    def decompress(self, path):
        """
        decompress the zip file and return the stuff that create from the decompress process
        """
        current_time = dt.datetime.now()
        #incase the whole decompress take more than 5 min
        prev = current_time-dt.timedelta(minutes=5)
        res = []
        with ZipFile(path, 'r') as f:
            f.extractall("./")
        for item in os.listdir("./"):
            files = osp.join("./",item)
            if osp.isfile(files):
                st = os.stat(files)
                mtime = dt.datetime.fromtimestamp(st.st_mtime)
                if mtime > prev:
                    res.append(files)
        return res

class tarDecompressor(compressDecorator):
    pass

class jsonLoader(loadDecorator):
    
    """
    Read in default zip file, unzip and load the json file into memory
    """
    def load(self, fname):
        try:
            with open(fname, 'rb') as f:
                target = json.load(f)
            return target
        except FileNotFoundError as e:
            return e

class csvLoader(loadDecorator):
    """
    possible csv format implementation.
    """
    pass



class dataLoader(object):
    
    def __init__(self, path):
        self.l = loader()
        self.data = []
        self.path = path
    
    def load(self):
        file_list = []
        for item in os.listdir("./"):
            filename = osp.join("./",item)
            if osp.isfile(filename):
                if filename.endswith(".zip"):
                    self.l = zipDecompressor(self.l)
                    file_list.append(filename)
                elif filename.endswith("gz"):
                    self.l = tarDecompressor(self.l)
                    file_list.append(filename)
            if len(file_list) == 0:
                raise FileNotFoundError
        try:
            for filename in file_list:
                decompress_list = self.l.decompress(filename)
                for decompress_file in decompress_list:
                    if decompress_file.endswith("json"):
                        self.l = jsonLoader(self.l)
                    elif decompress_file.endswith("csv"):
                        self.l = csvLoader(self.l)
                    try:
                        self.data += self.l.load(decompress_file)
                    except ValueError:
                        print("flat file error")
        except FileNotFoundError:
            print("Decompress target does not exist")





if __name__ == "__main__":
    l = loader()
    path = ""
    res = []
    for fname in os.listdir('./'):
        if fnmatch(fname, "*.zip"):
            decompress = zipDecompressor(l)
            path = fname
    print(path)
    decompress_list = decompress.decompress(path)
    for decompress_file in decompress_list:
        if decompress_file.endswith(".json"):
            dataloader = jsonLoader(l)
            target = dataloader.load(decompress_file)
            res += target

    dl = dataLoader("./")
    dl.load()
    print(dl.data[:1])

