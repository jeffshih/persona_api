from posix import listdir
import sys
sys.path.append("./")
from src.config import *
import os
import json
from zipfile import BadZipFile, ZipFile
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


    def decompress(self,filename):
        pass 

    def load(self,filename):
        pass


class loadDecorator(loader):
    
    __loader: loader = None 
    SOURCE = compress_file_path
    TARGET = decompressed_file_path
    
    def __init__(self, loader:loader):
        self.__loader = loader

    @property
    def loader(self):
        return self.__loader


    def load(self,filename):
        return self.__loader.load(filename)

    def decompress(self,filename):
        return self.__loader.decompress(filename) 

class zipDecompressor(loadDecorator):

    def decompress(self, filename):
        """
        decompress the zip file and return the filename that create after the decompress process
        """
        current_time = dt.datetime.now()
        #incase the whole decompress take more than 5 min
        prev = current_time-dt.timedelta(minutes=5)
        res = []
        try:
            with ZipFile(filename, 'r') as f:
                f.extractall(self.TARGET)
        except BadZipFile as e:
            print("{}".format(e))
            return res
        for item in os.listdir(self.TARGET):
            files = osp.join(self.TARGET,item)
            if osp.isfile(files):
                st = os.stat(files)
                mtime = dt.datetime.fromtimestamp(st.st_mtime)
                if mtime > prev:
                    res.append(files)
        #print("using zip decompressor")
        return res

class tarDecompressor(loadDecorator):
    pass

class restartDecompressor(loadDecorator):
    def decompress(self, filename):
        res = [osp.join(self.TARGET, item) for item in os.listdir(self.TARGET)]
        if res:
            #print("using restart decompressor")
            return res
        else:
            return super().decompress(filename)

class jsonLoader(loadDecorator):
    
    """
    Read in default zip file, unzip and load the json file into memory
    """
    def load(self, fname):
        #print("using jsonLoader")
        try:
            with open(fname, 'rb') as f:
                target = json.load(f)
            return target
        except ValueError as e:
            print("Decoding Json failed")
            return {}

class csvLoader(loadDecorator):
    """
    possible csv format implementation.
    """
    pass



class dataLoader(object):
    
    def __init__(self, source = compress_file_path, target = decompressed_file_path):
        self.loader = loader()
        self.data = []
        if not osp.isdir(source) or not osp.isdir(target):
            raise PermissionError
        self.__source = source
        self.__target = target
        self.__load()
        if not self.data:
            raise FileNotFoundError

    def __load(self):
        file_list = []
        for item in os.listdir(self.__source):
            filename = osp.join(self.__source,item)
            if osp.isfile(filename):
                if filename.endswith(".zip"):
                    self.loader = zipDecompressor(self.loader)
                    file_list.append(filename)
                elif filename.endswith("gz"):
                    self.loader = tarDecompressor(self.loader)
                    file_list.append(filename)
        if len(file_list) == 0:
            raise FileNotFoundError
        if len(os.listdir(self.__target)) != 0:
            self.loader = restartDecompressor(self.loader)
        try:
            for filename in file_list:
                decompress_list = self.loader.decompress(filename)
                if not decompress_list:
                    raise BadZipFile
                for decompress_file in decompress_list:
                    if decompress_file.endswith("json"):
                        self.loader = jsonLoader(self.loader)
                    elif decompress_file.endswith("csv"):
                        self.loader = csvLoader(self.loader)
                    try:
                        self.data += self.loader.load(decompress_file)
                    except ValueError:
                        print("loader decorate error")
        except FileNotFoundError:
            print("Decompress target does not exist")




if __name__ == "__main__":
    """
    dl = loader()
    path = ""
    res = []
    for fname in os.listdir('./'):
        if fnmatch(fname, "*.zip"):
            dl = zipDecompressor(dl)
            path = fname
    #dl = restartDecompressor(dl)
    print(path)
    decompress_list = dl.decompress(path)
    for decompress_file in decompress_list:
        if decompress_file.endswith(".json"):
            dl = jsonLoader(dl)
            target = dl.load(decompress_file)
            res += target
    """
    dl = dataLoader("./temp")
    