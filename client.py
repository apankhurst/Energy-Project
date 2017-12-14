import json
import requests
import sys

from checking import valid_datetime

def get_by_name(level, name):
    if levels[level] is None:
        print("level doesn't exist")
        return {}
    
    lev = levels[level]
    select = {}
    
    for l in lev:
        if l['name'] == name:
            select = l
            break
        
    if select == {}:
        print(name + " doesn't exist")
    return select

def contact_endpoint(endpoint,level,name,filters):
    select = get_by_name(level,name)
    if select == {}:
        return 
    
    ip = select['ip']
    port = select['port']
    
    try:
        print("date format: %Y-%m-%dT%H:%M")
        s = input('please enter a start date: ')
        start = valid_datetime(s)
        
        e = input('please enter an end date: ')
        end = valid_datetime(s)

        if(s >= e):
            print('please make sure your dates are in the right order')
            return

        url_str = "http://"+ip+":"+port+endpoint
        payload = "?start="+s+"&end="+e

        if filters is not None:
            payload += filters


        print(url_str+payload)
        r = requests.get(url_str+payload)
        return r.json
        
    except ValueError:
        return 

def print_levels():
    for level in levels:
        if levels[level]:
            print(level)

def view(level):
    for l in levels[level]:
        print(l['name'])


def energy(level,name,appliances):
    filters = None
    if appliances:
        filters = "&types="+",".join(appliances)
    
    response = contact_endpoint("/appliances/all",level,name,filters)
    print("Total Devices: " + response['appliances_count'])
    print("Total Energy Usage: " + response['total_energy'])
    print("Average Energy Usage: " + response['average_energy'])

def power(level,name,appliances):
    filters = '&power=True'
    if appliances:
        filters = "&types="+",".join(appliances)
        
        response = contact_endpoint("/appliances/all",level,name,filters)
        print("Total Devices: " + response['appliances_count'])
        print("Total Power Usage: " + response['total_power'])
        
def help():
    print('levels - print the levels available for query')
    print('view <level> - view all available elements at <level>')
    print('energy <level> <name> <app1> ... - get number of appliances and total energy useage for specified appliances')
    print('power <level> <name> <app1> ... - get number of appliances and total energy useage for specified appliances') 
    print('quit')

if len(sys.argv) < 2:
    print('usage: python client.py <config.json>')

levels = {}

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
