# this is a module that implements functions for checking formats of parameters
from datetime import datetime

def valid_datetime(dt):
    dt_format = "%Y-%m-%dT%H:%M"

    try:
        datetime.strptime(dt, dt_format)
    except ValueError:
        return False

    current = datetime.now().strftime(dt_format)
    
    return dt <= current

def tests():
    test_1 = "2012-12-19T06:01"  
    print(test_1 + " : " + str(valid_datetime(test_1)))
    test_2 = "2018-12-19T06:01"
    print(test_2 + " : " + str(valid_datetime(test_1)))
tests()
