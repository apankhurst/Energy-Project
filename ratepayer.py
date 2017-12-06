import pymongo
import flask
import json
import optparse
from urllib.parse import quote_plus
from flask import Flask
from flask import request
from pymongo import MongoClient
from checking import valid_datetime
from datetime import datetime

format_string = "%Y-%m-%dT%H:%M"

app = Flask(__name__)

username = "root"
password = "CyeX6L2e19AT"
hostname = ""
uri = "mongodb://%s:%s@ec2-54-165-229-239.compute-1.amazonaws.com/ratepayer_db?authsource=admin" % (
    quote_plus(username), quote_plus(password))
# Should remove connect=True after testing is done
client = MongoClient(uri)

db = client['ratepayer_db']
applicance_collection = db['appliances']


# allow appliance to update the data base
# data will come in the form
# appliance_id, start_time, end_time, energy_usage
# def post_data(self, app_type, name, start, end, value):

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
    start_date = valid_datetime(request.args.get('start'))
    end_date = valid_datetime(request.args.get('end'))
    energy = request.args.get('energy')
    print(str(type(start_date)))

    # check all parameters exist
    if (appliance_id is None or
                start_date is None or
                end_date is None or energy is None):
        return 'ARGUMENT ERROR: Missing arguments'

    # check if all parameters are valid
    if int(energy) < 0:
        return 'ARGUMENT ERROR: Energy below 0'

    try:
        if db.appliances.find({'app_id': appliance_id}) is None:
            db.appliances.insert({'app_id': appliance_id, 'type': 'unknown'})

        this_appliance = db.get_collection(str(appliance_id))
        result = this_appliance.insert_one({
            'start': start_date,
            'end': end_date,
            'energy': energy
        })
    except:
        print("Error")

    return "success"

@app.route('/appliance/<appliance_id>')
def get_total_for_time_window(appliance_id):
    assert str(appliance_id) in db.collection_names(), 'The database does not have any data for the given appliance'
    start = valid_datetime(request.args.get('start'))
    end = valid_datetime(request.args.get('end'))

    total = 0.0
    try:
        this_appliance = db.get_collection(str(appliance_id))
        returned_entries = this_appliance.find({'start':{'$gte': start}, 'end':{'$lte':end}})

        for e in returned_entries:
            print (str(e))
            total = total + float(e['energy'])
    except:
        print("error")
        return "error"

    return "Total energy:" + str(total)

def get_database_info(info_file):
    # json file that stores all of the info for the
    with open(info_file) as json_data:
        database_info = json.load(json_data)

    return database_info
