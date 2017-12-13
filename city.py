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
        
app = Flask(__name__)

@app.route('/total')
def total():

    start = valid_datetime(request.args.get('start'))
    end = valid_datetime(request.args.get('end'))

    start_str = start.strftime("%Y-%m-%dT%H:%M")
    end_str = end.strftime("%Y-%m-%dT%H:%M")

    if(start_str >= end_str):
        return 'Incorrect dates'
    
    total = 0.0
    for rp in ratepayers:
        url_str = 'http://' + rp + ":" + ratepayers[rp] + "/total?"
        payload = "start="+start_str+"&end="+end_str

        r = requests.get(url_str+payload)
        response = r.json()

    return 'thank you, come again'

@app.route('/appliance/all')
def by_appliance_type():

    total_apps = 0
    total_enrg = 0.0
    
    start = valid_datetime(request.args.get('start'))
    end = valid_datetime(request.args.get('end'))  

    type_selected = False

    if(start_str >= end_str):
        return 'Incorrect dates'  

    try:
        required_types = request.args.get('types').split(',')
        type_selected = True
    except:
        type_selected = False
        
    for rp in ratepayers:
        url_str = 'http://'+rp+":"+ratepayers[rp]+"/appliance/all"

        if type_selected:
            url_str += "?" + required_types
        
        r = request.get(url+payload)
        response = r.json()
        total_apps += int(response['appliances_count'])
        total_enrg += float(response['total_energy'])

    final_info = {'appliances_count': total_apps, 'total_energy': total_enrg}
    return json.dumps(final_info) 
        
    return 'thank you, come again'
if __name__ == '__main__':
    app.run()
