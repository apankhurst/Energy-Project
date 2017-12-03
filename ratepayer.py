import pymongo
import flask

from pymongo import MongoClient

database_name = 'db'

class RatePayer:
    def __init__(self):
        # Create a client and get the database
        self.client = MongoClient()
        self.appliace_db = self.client['db']
