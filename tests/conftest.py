import sys
sys.path.append("./")
from src.config import *
from src.dataloader import dataLoader
from src.database import database
import pytest 

@pytest.fixture
def dl_t():
    path = './'
    dl_t = dataLoader()
    yield dl_t
    del dl_t

@pytest.fixture
def db_t():
    db_t = database()
    yield db_t
    del db_t