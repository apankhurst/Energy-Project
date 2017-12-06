import pymongo
import flask
import json
import optparse
import checking

from flask import Flask
from flask import request
from pymongo import MongoClient

# json file that stores all of the info for the 
database_info_file = 'ratepayers/ratepayer1.json'

with open(database_info_file) as json_data:
    database_info = json.load(json_data)


app = Flask(__name__)





client = MongoClient("mongodb://root:CyeX6L2e19AT@ec2-54-165-229-239.compute-1.amazonaws.com:27017")
db = client['ratepayer_db']
applicance_collection = db['appliances']
#print(appliance_db.get_collection('app'))

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

# allow home appliances to submit data to the ratepayer with the REST API
@app.route('/submit')
def record_data():
    # get the passed parameters
    appliance_id = request.args.get('id')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    energy = request.args.get('energy')

    # check all parameters exist
    if (appliance_id is None or
        start_date is None or
        end_date is None or energy is None):
        return 'ARGUMENT ERROR'

    
    # check if all parameters are valid
    if (!(valid_datetime(start_date)) or
        !(valid_datetime(end_date)) or
        start_date >= end_date or energy < 0):
        return 'ARGUMENT ERROR'
    

    record = {
        'start': start_date,
        'end': end_date,
        'energy': energy
    }

    try:
        this_appliance = db.get_collection(appliance_id + str())
        this_appliance.insert_one(record)

    except:
        print("Error")

    retval = appliance_id
    return retval
