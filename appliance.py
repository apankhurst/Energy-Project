import requests

class Appliance:
    def __init__(self, app_type, app_id, host_name):
        self.app_type = app_type
        self.app_id = app_id
        self.host_name = host_name
        self.host_port = 5000
        
        def post_usage(self, start, end, energy):
            host_str = 'http://' + str(self.host_name) + ':' + str(self.host_port) + '/submit'
            payload = {'id': str(self.app_id),'start': str(start),'end=': str(end),'energy': str(energy)}
            
            r = requests.get(host_str,params=payload)
            print(r.url)
            
            a = Appliance(1,2,'137.165.172.11')
            a.post_usage('now','later','alot')

a = Appliance(1,1,'137.165.172.11')
a.post_usage('a','b','c')
