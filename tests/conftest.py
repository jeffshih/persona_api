import sys
sys.path.append("./")
from src.config import *
from src.dataloader import dataLoader
from src.database import database
from src.main import create_app
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

@pytest.fixture
def app_t():
    app_t = create_app()
    yield app_t.test_client()
    del app_t
