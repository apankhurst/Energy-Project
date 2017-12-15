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

@app.route('/appliances/all')
def by_appliance_type():

    total_apps = 0
    total =  0.0
    
    start = valid_datetime(request.args.get('start'))
    end = valid_datetime(request.args.get('end'))  
    return_power = request.args.get('power')

    if return_power == 'true':
        return_power = True
    else:
        return_power = False
    
    start_str = start.strftime("%Y-%m-%dT%H:%M")
    end_str = end.strftime("%Y-%m-%dT%H:%M") 
    
    type_selected = False

    if(start_str >= end_str):
        return 'Incorrect dates'  

    try:
        required_types = request.args.get('types')
        type_selected = True
    except:
        type_selected = False

    for rp in ratepayers:
        url_str = 'http://'+rp+":"+ratepayers[rp]+"/appliance/all"
        payload = "?start="+start_str+"&end="+end_str

        print(url_str+payload)

        if required_types is not None:
            payload += "&types=" + required_types
        if return_power:
            payload += "&power=True"
            
        r = requests.get(url_str+payload)
        response = r.json()

        if return_power:
            total += float(response['total_power'])
        else:
            total += float(response['total_energy'])

        total_apps += int(response['appliances_count'])

        
    if return_power:
        final_info = {'appliances_count': total_apps, 'total_power': total}
    else:
        final_info = {'appliances_count': total_apps, 'total_energy': total} 

    return json.dumps(final_info) 
        
if __name__ == '__main__':
    app.run()
