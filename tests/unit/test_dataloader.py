import sys 
sys.path.append("./")
from src.dataloader import *
import json
import random
import pytest

@pytest.fixture(scope="module")
def dl():
    path = './'
    dl = dataLoader(path)
    dl.load()
    yield dl
    del dl


def test_dataloader(dl):
    """
    decompressor should return a list of file that decompressed into json or csv
    """
    res = dl.data[:1]
    expected = [{'job': 'Solicitor', 'company': 'Smith, Haynes and Hooper', 'ssn': 'ZZ376803T', 'residence': '1 Bruce alley\nNew Justin\nL07 2TE', 'current_location': [-66.491849, -69.512524], 'blood_group': 'AB+', 'website': ['https://www.holmes-saunders.com/', 'http://foster-ford.com/', 'https://www.farrell-evans.com/', 'http://white-kelly.net/'], 'username': 'mauriceharris', 'name': 'Dr. Mohamed Newton', 'sex': 'F', 'address': '09 Knight parkways\nWest Yvonneshire\nHD23 5NJ', 'mail': 'jshort@hotmail.com', 'birthdate': '1989-07-07'}]
    assert res == expected

def test_dataformat(dl):
    """
    test the extracted data is in the correct format, which can form a dict and have all the target key
    """
    keys = ['job','company','ssn','residence','current_location','blood_group','website','username','name','sex','address','mail','birthdate']
    target = random.choice(dl.data)
    assert isinstance(target,dict)
    k = target.keys()
    for key in keys:
        assert key in k

