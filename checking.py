# this is a module that implements functions for checking formats of parameters
from datetime import datetime

def valid_datetime(dt):
    try:
        datetime.strptime(dt,"%Y-%m-%dT%H:%M")
        return True
    except ValueError:
        return False

def tests():
    test_1 = "2012-12-19T06:01"  
    print(test_1 + " : " + str(valid_datetime(test_1)))
    test_2 = "2018-12-19T06:01"
    print(test_2 + " : " + str(valid_datetime(test_1)))
tests()
