import os

from petisco.persistence.pymongo.pymongo_persistence_config import (
    PyMongoPersistenceConfig,
)
from petisco.persistence.pymongo.pymongo_persistence_connector import (
    PyMongoPersistenceConnector,
)


def config_mongo_persistence():
    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    port = int(os.getenv("MONGODB_PORT"))
    host = os.getenv("MONGODB_HOST")
    database = os.getenv("MONGODB_DATABASE")
    mongodb_config = PyMongoPersistenceConfig(
        host=host, user=username, password=password, port=port, database=database
    )
    mongodb_persistence_connector = PyMongoPersistenceConnector(config=mongodb_config)
    mongodb_persistence_connector.execute()
