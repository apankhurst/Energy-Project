import pymongo
import flask

from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

database_name = 'db'

client = MongoClient("mongodb://root:CyeX6L2e19AT@ec2-54-165-229-239.compute-1.amazonaws.com:27017")
appliance_db = client['ratepayer_db']
applicance_collection = appliance_db['appliances']

# allow appliance to update the data base
# data will come in the form
# appliance_id, start_time, end_time, energy_usage
#def post_data(self, app_type, name, start, end, value):

@app.route('/')
def test_method():
    return 'Hi Ari'

@app.route('/hello/<name>')
def test_name(name):
    return 'hello ' + str(name)

