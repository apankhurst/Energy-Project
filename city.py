import flask
import json
import requests

from flask import Flask
from flask import request
from checking import valid_datetime

ratepayers = {}

# This file contains a list of the IPs
# of the rate payers below the city
init_file = "city_config.json"

with open(init_file) as json_data:
    info = json.load(json_data)
    
    for r in info['ratepayers']:
        ip = r['ip']
        port = r['port']
        ratepayers[ip] = port
        
app = Flask(__name__)

# this end point will gather all of the requested data from
# the ratepayers below it and send it as a json object to the requester
@app.route('/appliances/all')
def by_appliance_type():

    total_apps = 0 # total number of appliances
    total =  0.0 # total energy/power used

    # get the parameters from the request
    start = valid_datetime(request.args.get('start'))
    end = valid_datetime(request.args.get('end'))  
    return_power = request.args.get('power')

    if return_power == 'true':
        return_power = True
    else:
        return_power = False
    
    start_str = start.strftime("%Y-%m-%dT%H:%M")
    end_str = end.strftime("%Y-%m-%dT%H:%M") 

    # determine if the dates are correct
    if(start_str >= end_str):
        return 'Incorrect dates'  

    required_types = request.args.get('types')

    # construct the API call and send it to each ratepayer
    # get the responses and aggregate them
    for rp in ratepayers:
        url_str = 'http://'+rp+":"+ratepayers[rp]+"/appliances/all"
        payload = "?start="+start_str+"&end="+end_str

        if required_types is not None:
            payload += "&types=" + required_types
        if return_power:
            payload += "&power=true"

        r = requests.get(url_str+payload)
        response = r.json()

        if return_power:
            total += float(response['total_power'])
        else:
            total += float(response['total_energy'])

        total_apps += int(response['appliances_count'])

    # send the response to the caller
    if return_power:
        final_info = {'appliances_count': total_apps, 'total_power': total}
    else:
        final_info = {'appliances_count': total_apps, 'total_energy': total} 

    return json.dumps(final_info) 
        
if __name__ == '__main__':
    app.run()
