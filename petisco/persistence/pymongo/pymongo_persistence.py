from pymongo import MongoClient

from petisco.application.singleton import Singleton


class PyMongoPersistence(metaclass=Singleton):
    @staticmethod
    def get_instance():
        return PyMongoPersistence()

    def __init__(self, client: MongoClient = None, database: str = None):
        self.client = client
        self.database = database
