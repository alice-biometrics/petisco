from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from petisco.persistence.interface_persistence_connector import IPersistenceConnector
from petisco.persistence.pymongo.pymongo_persistence import PyMongoPersistence
from petisco.persistence.pymongo.pymongo_persistence_config import (
    PyMongoPersistenceConfig,
)


class PyMongoPersistenceConnector(IPersistenceConnector):
    def __init__(self, config: PyMongoPersistenceConfig):
        self.config = config

    def execute(self):
        if not self.config.database:
            raise ValueError(
                "Petisco PyMongoPersistenceConnector is not configured correctly. "
                "Please check PyMongoPersistenceConfig and add database name"
            )

        mongo_client = MongoClient(
            f"mongodb://{self.config.host}:{self.config.port}/",
            username=self.config.user,
            password=self.config.password,
        )
        try:
            # The ismaster command is cheap and does not require auth.
            mongo_client.admin.command("ismaster")
        except ConnectionFailure:
            raise ConnectionError(
                "Petisco PyMongoPersistenceConnector can't connect to MongoDB. "
                "Please check PyMongoPersistenceConfig and add required values"
            )
        PyMongoPersistence(client=mongo_client, database=self.config.database)
