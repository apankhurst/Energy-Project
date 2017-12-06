import json
import requests

class Appliance:
        def __init__(self, host_name, host_port, info):
            # json file that stores all of the info for the

                
                self.type = info['type']
                self.id = info['id']
                self.host_name = host_name
                self.host_port = host_port
                
        def post_usage(self, start, end, energy):
            host_str = 'http://' + self.host_name + ':' + self.host_port + '/submit'
            payload = {'id': self.app_id,'start': str(start),'end=': str(end),'energy': str(energy)}
        
            r = requests.get(host_str,params=payload)
            print(r.url)      
                    
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

h = Home('homes/home1.json')
