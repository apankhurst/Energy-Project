import json
import requests
import sys

from checking import valid_datetime

if len(sys.argv) < 2:
    print('usage: python client.py <config.json>')

levels = {}

config_file = sys.argv[1]
with open(config_file) as json_data:
    info = json.load(json_data)
    for level in info:
        levels[level] = info[level]
    
def print_levels():
    for level in levels:
        if levels[level]:
            print(level)

def view(level):
    for l in levels[level]:
        print(l['name'])

def appliances(level,name,appliances):
    if levels[level] is None:
        print("level doesn't exist")
        return 

    lev = levels[level]
    select = {}
    
    for l in lev:
        if l['name'] == name:
            select = l
            break

    if select == {}:
        print(name + " doesn't exist")
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

        url_str = "http://"+ip+":"+port+"/appliance/all"
        payload = "?start="+s+"&end="+e

        if appliances:
            payload += "&types="+",".join(appliances)
            
        print(url_str+payload)
            
    except ValueError:
        return 

def help():
    print('levels - print the levels available for query')
    print('view <level> - view all available elements at <level>')
    print('appliances <level> <name> <app1> ... - get number of appliances and total energy useage for specified appliances')
    print('quit')
    
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
        elif c == 'appliances':
            if len(ans) > 2:
                appliances(ans[1], ans[2], ans[3:])
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
