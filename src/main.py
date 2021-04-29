from src.config import *
from flask import Flask
from flask import jsonify
from flask import request



app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello'

