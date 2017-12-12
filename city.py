import flask
import json
import requests

from flask import Flask
from flask import request

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
    total = 0.0
    for rp in ratepayers:
        host_str = 'http://' + rp + ":" + ratepayers[rp] + "/total"
        print(host_str)


if __name__ == '__main__':
    app.run()
