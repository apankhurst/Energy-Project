import pymongo
import flask

from flask import Flask
from flask import request
from pymongo import MongoClient

app = Flask(__name__)

database_name = 'db'

client = MongoClient("mongodb://root:CyeX6L2e19AT@ec2-54-165-229-239.compute-1.amazonaws.com:27017")
appliance_db = client['ratepayer_db']
applicance_collection = appliance_db['appliances']
print(appliance_db.get_collection('app'))

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

@app.route('/submit')
def record_data():
    appliance_id = request.args.get('id')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    energy = request.args.get('value')

    if appliance_id is None or start_date is None or end_date is None or energy is None:
        return 'ERROR'

    retval = appliance_id + start_date + end_date + energy
    return retval