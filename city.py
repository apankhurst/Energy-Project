import sys
import flask
import json
import csv

from flask import Flask
from flask import request

# This file contains a list of the IPs
# of the rate payers below the city
ratepayer_ips = []

config_file = "test.txt"
open_file = open(config_file, "r")









app = Flask(__name__)

@app.route('/submit')
def record_data():
    appliance_id = request.args.get('id')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    energy = request.args.get('energy')

    if appliance_id is None or start_date is None or end_date is None or energy is None:
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

if __name__ == '__main__':
    app.run()
