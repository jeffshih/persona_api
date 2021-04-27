import sys 
sys.path.append("./")
from src.db import db


d = db()

print(d.desc())
