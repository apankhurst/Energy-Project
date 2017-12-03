import pymongo
import flask

from flask import Flask
from pymongo import MongoClient

#app = Flask(__name__)

database_name = 'db'

client = MongoClient()
appliance_db = client[database_name]

# allow appliance to update the data base
# data will come in the form
# appliance_id, start_time, end_time, energy_usage
def post_data(self, app_type, name, start, end, value):
        
