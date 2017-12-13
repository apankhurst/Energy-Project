import flask
import json
import requests

from flask import Flask
from flask import request
from checking import valid_datetime

# This file contains a list of the IPs
# of the rate payers below the city
ratepayers = {}

init_file = "city_config.json"
with open(init_file) as json_data:
    info = json.load(json_data)
    
    for r in info['ratepayers']:
        ip = r['ip']
        port = r['port']
        ratepayers[ip] = port

for r in ratepayers:
    print(r + " " + ratepayers[r])
        
app = Flask(__name__)

@app.route('/total')
def total():

    start = valid_datetime(request.args.get('start'))
    end = valid_datetime(request.args.get('end'))

    start_str = start.strftime("%Y-%m-%dT%H:%M")
    end_str = end.strftime("%Y-%m-%dT%H:%M")
    
    total = 0.0
    for rp in ratepayers:
        url_str = 'http://' + rp + ":" + ratepayers[rp] + "/total?"
        payload = "start="+start_str+"&end="end_str
        print(url_str+payload)


if __name__ == '__main__':
    app.run()
