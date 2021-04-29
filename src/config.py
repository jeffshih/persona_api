import os
import sys

"""
basic configuration
"""
APP_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
sys.path.append(PROJECT_ROOT)
compress_file_path = PROJECT_ROOT
decompressed_file_path = os.path.join(PROJECT_ROOT,"storage")




