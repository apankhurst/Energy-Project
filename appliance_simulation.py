import sys
import json
import requests
import datetime
import urllib
import random

from time import sleep

class Appliance:
        def __init__(self, host_name, host_port, info):
                self.type = info['type']
                self.id = info['id']
                self.current_date = datetime.datetime.strptime(info['start'], "%Y-%m-%dT%H:%M")
                self.end_date = datetime.datetime.strptime(info['end'], "%Y-%m-%dT%H:%M")
                self.host_name = host_name
                self.host_port = host_port
                self.min = int(info['min'])
                self.max = int(info['max'])

        def can_post(self):
                return self.current_date < self.end_date                

        def post_next(self):

                time = random.randint(7,13)
                energy = random.random(self.min, self.max)
                start = self.current_date
                end = self.current_date + datetime.timedelta(seconds=60*time)

                if(end > self.end_date):
                        end = self.end_date
                        
                start_str = start.strftime("%Y-%m-%dT%H:%M")
                end_str = end.strftime("%Y-%m-%dT%H:%M")
                
                self.current_date = end
                url_str = 'http://'+self.host_name+":"+self.host_port+"/submit?"
                payload = "id="self.id+"&start="+str(start_str)+"&end="+str(end_str)+"&energy="+str(energy) 
                r = requests.get(url_str+payload)
                
class Home:
        def __init__(self, init_file):
        # json file that stores all of the info for the
                self.appliances = []
                
                with open(init_file) as json_data:
                        info = json.load(json_data)
                home_name = info['home_name']
                home_port = info['home_port']
                for app in info['appliances']:
                        self.appliances.append(Appliance(home_name, home_port, app))

if len(sys.argv < 2):
        print 'usage: python appliance_simulation.py <config.json>'
                        
config_file = sys.argv[1]
h = Home(config_file)

while h.appliances:
        for app in h.appliances:
                if app.can_post():
                        app.post_next()
                else:
                        h.appliances.remove(app)
                sleep(0.1)
                
