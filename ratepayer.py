import pymongo
import flask
import json
import optparse
import checking
from urllib.parse import quote_plus
from flask import Flask
from flask import request
from pymongo import MongoClient
from checking import valid_datetime

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
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    energy = request.args.get('energy')

    # check all parameters exist
    if (appliance_id is None or
                start_date is None or
                end_date is None or energy is None):
        return 'ARGUMENT ERROR: Missing arguments'

    # check if all parameters are valid
    if (not valid_datetime(start_date) or
            not valid_datetime(end_date) or
                start_date >= end_date or int(energy) < 0):
        return 'ARGUMENT ERROR: Invalid dates'


    try:
        this_appliance = db.get_collection(str(appliance_id))
        result = this_appliance.insert_one({
        'start': start_date,
        'end': end_date,
        'energy': energy
    })
    except:
        print("Error")

    retval = appliance_id
    return retval


def get_database_info(info_file):
    # json file that stores all of the info for the
    with open(info_file) as json_data:
        database_info = json.load(json_data)

    return database_info
