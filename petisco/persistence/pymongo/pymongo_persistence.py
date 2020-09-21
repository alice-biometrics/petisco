from pymongo import MongoClient
from pymongo.database import Database

from petisco.application.singleton import Singleton


class PyMongoPersistence(metaclass=Singleton):
    @staticmethod
    def get_instance():
        return PyMongoPersistence()

    def __init__(self, client: MongoClient = None, database: Database = None):
        self.client = client
        self.database = database
