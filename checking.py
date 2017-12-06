# this is a module that implements functions for checking formats of parameters
from datetime import datetime


# check if a passed date and time is value
# a datetime will be invalid if it doesn't fit the standard format or if it is
# larger than the current date
def valid_datetime(dt):

    # the ISODate format string
    dt_format = "%Y-%m-%dT%H:%M"

    # check date and time meet the necessary format
    try:
        datetime.strptime(dt, dt_format)
    except ValueError:
        return False

    # check the date & time are not in the future
    current = datetime.now().strftime(dt_format)

    return dt <= current
