import os

import pytest

from petisco.persistence.pymongo.mongodb_is_running_locally import (
    mongodb_is_running_locally,
)
from petisco.persistence.pymongo.pymongo_persistence import PyMongoPersistence
from petisco.persistence.pymongo.pymongo_persistence_config import (
    PyMongoPersistenceConfig,
)
from petisco.persistence.pymongo.pymongo_persistence_connector import (
    PyMongoPersistenceConnector,
)

username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
port = int(os.getenv("MONGODB_PORT"))
host = os.getenv("MONGODB_HOST")
database = os.getenv("MONGODB_DATABASE")


@pytest.mark.integration
@pytest.mark.skipif(
    not mongodb_is_running_locally(
        host=host, username=username, password=password, port=port
    ),
    reason="MongoDB is not running locally",
)
def test_should_initialize_persistence():
    config = PyMongoPersistenceConfig(
        user=username, password=password, port=port, host=host, database=database
    )
    connector = PyMongoPersistenceConnector(config=config)
    connector.execute()
    persistence = PyMongoPersistence.get_instance()
    persistence.client.server_info()
    persistence.client.close()
