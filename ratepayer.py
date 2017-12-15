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

init_file = "ratepayer_config.json"

username = ""
password = ""
uri = ""
database = ""
collection = ""

with open(init_file) as json_data:
    info = json.load(json_data)
    username = info['username']
    password = info['password']
    uri = info['uri'] % (quote_plus(username), quote_plus(password))
    database = info['database']
    collection = info['collection']

#DELETE THIS LATER
"""    
username = "root"
password = "CyeX6L2e19AT"
hostname = ""
uri = "mongodb://%s:%s@ec2-54-165-229-239.compute-1.amazonaws.com/ratepayer_db?authsource=admin" % (
    quote_plus(username), quote_plus(password))
"""
# Should remove connect=True after testing is done
client = MongoClient(uri)

db = client[database]
applicance_collection = db[collection]


# allow appliance to update the data base
# data will come in the form
# appliance_id, start_time, end_time, energy_usage
# def post_data(self, app_type, name, start, end, value):


# allow ratepayer's appliances to submit data to the ratepayer with the REST API
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
    if float(energy) < 0:
        return 'ARGUMENT ERROR: Energy below 0'

    try:
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

#Get energy sum for a specific appliance ID belonging to this ratepayer.
#Start and end date must be supplied in the query string.
@app.route('/appliance/<appliance_id>')
def get_total_for_time_window(appliance_id):
    assert str(appliance_id) in db.collection_names(), 'The database does not have any data for the given appliance'
    start = valid_datetime(request.args.get('start'))
    end = valid_datetime(request.args.get('end'))

    assert start<=end, "start date must be before end"

    total = 0.0
    appliance_type = ''
    try:
        metadata = db.get_collection('appliances').find_one({'app_id': appliance_id})
        appliance_type = metadata['type']
    except:
        appliance_type = 'unknown'
    #filter energy records by time at the database before returning them to the application
    try:
        this_appliance = db.get_collection(str(appliance_id))
        returned_entries = this_appliance.find({'start':{'$gte': start}, 'end':{'$lte':end}})

        for e in returned_entries:
            print (str(e))
            total = total + float(e['energy'])
    except:
        print("error")
        return "error"
    #Create return string if the user requested power instead of energy
    if return_power == "true":
        timediff = (end - start)
        hours_in_window = (timediff.total_seconds()) / 3600.0
        print(str(hours_in_window))
        power = total / hours_in_window
        energy_info = {'appliance_id': appliance_id, 'appliance_type': appliance_type, 'power_total':power}
    #Create return string if the user did not specify that power should be returned instead of energy
    else:
        energy_info = {'appliance_id': appliance_id, 'appliance_type': appliance_type, 'energy_total':total}

    return json.dumps(energy_info)

#Get energy sum for all appliances belonging to this ratepayer.
#Start and end date must be supplied in the query string.
#If 'power=true' is supplied in the query string, power is returned instead of energy.
@app.route('/appliances/all')
def get_ratepayer_total():
    #Get query string parameters
    start = valid_datetime(request.args.get('start'))
    end = valid_datetime(request.args.get('end'))
    return_power = request.args.get('power')

    print(return_power)
    print(return_power == 'true')
    assert start <=end, "start date must be before end"
    type_selected = False
    try:
        #Allows user to specify a list of device types separated by commas
        required_types = request.args.get('types').split(',')
        type_selected = True
    except:
        type_selected = False

    total = 0.0
    appliances_count = 0
    try:
        for m in db.get_collection('appliances').find():
            if type_selected is False or(type_selected and m['type'] in required_types):
                appliances_count = appliances_count + 1
                this_appliance = db.get_collection(str(m['app_id'])).find({'start':{'$gte': start}, 'end':{'$lte':end}})
                for e in this_appliance:
                    total = total + float(e['energy'])
    except:
        print("error")
        return "error"
    #Create return string if the user requested power instead of energy
    if return_power == "true":
        timediff = (end - start)
        hours_in_window = (timediff.total_seconds()) / 3600.0
        print(str(hours_in_window))
        power = total / hours_in_window
        final_info = {'appliances_count': appliances_count, 'total_power': power}
    #Create return string if the user did not specify that power should be returned instead of energy
    else:
        final_info = {'appliances_count': appliances_count, 'total_energy': total}
    return json.dumps(final_info)


#Get list of all appliances belonging to this ratepayer.
#Appliance ID and appliance type are returned for each appliance.
#No energy data is returned.
@app.route('/appliances/list')
def list_appliances():
    appliances_list = []
    try:
        for m in db.get_collection('appliances').find():
            appliances_list.append({'appliance_id': m['app_id'], 'type':m['type']})

    except:
        print('error')

    return json.dumps(appliances_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
