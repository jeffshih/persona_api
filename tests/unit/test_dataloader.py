import sys
import os.path as osp
import os
sys.path.append("./")
APP_DIR = osp.abspath(osp.dirname(__file__))
PROJECT_ROOT = osp.abspath(osp.join(APP_DIR, os.pardir))
from src.dataloader import *
from src.config import *
import random
import pytest



def test_dataloader(dl_t):
    """
    decompressor should return a list of file that decompressed into json or csv
    """
    res = dl_t.data[:1]
    expected = [{'job': 'Solicitor', 'company': 'Smith, Haynes and Hooper', 'ssn': 'ZZ376803T', 'residence': '1 Bruce alley\nNew Justin\nL07 2TE', 'current_location': [-66.491849, -69.512524], 'blood_group': 'AB+', 'website': ['https://www.holmes-saunders.com/', 'http://foster-ford.com/', 'https://www.farrell-evans.com/', 'http://white-kelly.net/'], 'username': 'mauriceharris', 'name': 'Dr. Mohamed Newton', 'sex': 'F', 'address': '09 Knight parkways\nWest Yvonneshire\nHD23 5NJ', 'mail': 'jshort@hotmail.com', 'birthdate': '1989-07-07'}]
    assert res == expected

def test_dataformat(dl_t):
    """
    test the extracted data is in the correct format, which can form a dict and have all the target key
    """
    keys = ['job','company','ssn','residence','current_location','blood_group','website','username','name','sex','address','mail','birthdate']
    target = random.choice(dl_t.data)
    assert isinstance(target,dict)
    k = target.keys()
    for key in keys:
        assert key in k

def test_data_sequence(dl_t):
    """
    test the sequence of loading flat file is consitant for further pagination.
    """
    newLoader = dataLoader()
    start = random.randint(0,10000)
    end = random.randint(0,10000)
    assert(dl_t.data[start:end] == newLoader.data[start:end])

def test_zipDecompressor():
    l = loader()
    decompressor = zipDecompressor(l)
    decompressor.TARGET = decompressed_file_path
    decompressor.SOURCE = compress_file_path
    res = decompressor.decompress("./fake_profiles.zip")
    expected = [os.path.join(PROJECT_ROOT,'storage/fake_profiles.json')]
    assert(res == expected)

def test_dataLoader_error():
    with pytest.raises(PermissionError):
        l = dataLoader(source="./abc") 
    with pytest.raises(FileNotFoundError):
        l = dataLoader(source="./static")
    with pytest.raises(BadZipFile):
        l = dataLoader(source="./temp",target="./static")

def test_jsonLoader(dl_t):
    l = loader()
    l = jsonLoader(l)
    res = l.load("./temp/mock.json")
    assert(res == {})
    decompressor = zipDecompressor(l)
    decompressor.TARGET = decompressed_file_path
    path = decompressor.decompress("./fake_profiles.zip") 
    res = l.load(osp.join(PROJECT_ROOT,"storage/fake_profiles.json"))
    os.remove(path[0])
    expected = dl_t.data
    assert(res==expected)