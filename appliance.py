import requests
import json

class Appliance:
    def __init__(self, init_file):

        # json file that stores all of the info for the
        with open(init_file) as json_data:
            info = json.load(json_data)

        self.type = info['type']
        self.id = info['id']
        self.host_name = info['host_name']
        self.host_port = info['host_port']
        
        def post_usage(self, start, end, energy):
            host_str = 'http://' + self.host_name + ':' + self.host_port + '/submit'
            payload = {'id': self.app_id,'start': str(start),'end=': str(end),'energy': str(energy)}
            
            r = requests.get(host_str,params=payload)
            print(r.url)
            


