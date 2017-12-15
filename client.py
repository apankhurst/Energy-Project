"""
- this module provides a CLI for inteacting
with the DEDASS system
- all information regarding the levels that can
be contacted must be stored with in a .json file
"""


import json
import requests
import sys

from checking import valid_datetime

levels = {}

# check if there exists an element called name at the specified
# level
def get_by_name(level, name):
    # check level exists
    if levels[level] is None:
        print("level doesn't exist")
        return {}
    
    lev = levels[level]
    select = {}
    
    # check name exists
    for l in lev:
        if l['name'] == name:
            select = l
            break
    
    if select == {}:
        print(name + " doesn't exist")

    # return the element dictionary
    return select

# interact with a DEDASS endpoint
def contact_endpoint(endpoint,level,name,filters):

    # get information on level element
    select = get_by_name(level,name)
    if select == {}:
        return 

    # ip address and port to contact
    ip = select['ip']
    port = select['port']

    # get start and end dates
    try:
        print("date format: %Y-%m-%dT%H:%M")
        s = input('please enter a start date: ')
        start = valid_datetime(s)

        e = input('please enter an end date: ')
        end = valid_datetime(s)

        if(s >= e):
            print('please make sure your dates are in the right order')
            return

        # construct the endpoint and payload 
        url_str = "http://"+ip+":"+port+endpoint
        payload = "?start="+s+"&end="+e

        if filters is not None:
            payload += filters

        # contact the endpoint   
        print(url_str+payload)
        r = requests.get(url_str+payload)
        return r.json()


    except ValueError:
        return 

# print the available levels
def print_levels():
    for level in levels:
        if levels[level]:
            print(level)

# print elements available at a level
def view(level):
    try:
        for l in levels[level]:
            print(l['name'])
    except KeyError:
        print('no level with name ' + level)

# get the total # of devices for a level and
# their total energy usage
def energy(level,name,appliances):
    filters = None

    if len(appliances) > 0:
        filters = "&types="+",".join(appliances)
    try:
        response = contact_endpoint("/appliances/all",level,name,filters)
        print(response)

    except TypeError:
        print('error ocurred')
# get the total # of devices for a level and
# their total power usage
def power(level,name,appliances):
    filters = '&power=true'
    if len(appliances) > 0:
        filters += "&types="+",".join(appliances)
    try:
        response = contact_endpoint("/appliances/all",level,name,filters)
        print(response)


    except TypeError:
        print('error ocurred')

# print commands
def help():
    print('levels - print the levels available for query')
    print('view <level> - view all available elements at <level>')
    print('energy <level> <name> <app1> ... - get number of appliances and total energy useage for specified appliances')
    print('power <level> <name> <app1> ... - get number of appliances and total energy useage for specified appliances') 
    print('quit')

if len(sys.argv) < 2:
    print('usage: python client.py <config.json>')

# setup from config file
config_file = sys.argv[1]
with open(config_file) as json_data:
    info = json.load(json_data)
    for level in info:
        levels[level] = info[level]
    

    
print("Welcome to DEDASS!")
print("D.E.D.A.S.S")
print("E.N.A.G.T.Y")
print("D.E.T.G.O.S")
print("A.R.A.R.R.T")
print("S.G. .E.A.E")
print("S.Y. .G.G.M")
print(" . . .A.E. ")
print(" . . .T. . ")
print(" . . .I. . ")
print(" . . .O. . ")
print(" . . .N. . ")

print("\nfor help type help")

# get user input and perform query
while True:
    try:
        ans = input('> ').split(' ')
        c = ans[0]
        if c == 'help':
            help()
        elif c == 'levels':
            print_levels()
        elif c == 'view':
            if len(ans) > 1:
                view(ans[1])
            else:
                print('please provide parameter')
        elif c == 'energy':
            if len(ans) > 2:
                energy(ans[1], ans[2], ans[3:])
            else:
                print('please provide parameters')
        elif c == 'power':
            if len(ans) > 2:
                power(ans[1], ans[2], ans[3:])
            else:
                print('please provide parameters') 
        elif c == 'quit':
            print("Thank you for using DEDASS!")
            break
        else:
            print('command not recognized')
    except KeyboardInterrupt:
        print("\nThank you for using DEDASS!")
        break
