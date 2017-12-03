import pymongo
import flask

from pymongo import MongoClient

database_name = 'db'

class RatePayer:

    # Ratepayer constructor
    def __init__(self):
        # create a client and get the database
        self.client = MongoClient()
        self.appliace_db = self.client['db']

    # post data to the database
    def post_data(app_type, name, start, end, value):

    def get_by_id(app_id, start_time, end_time):
        
