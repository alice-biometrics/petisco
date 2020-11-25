from contextlib import contextmanager

from pymongo.errors import InvalidName, PyMongoError

from petisco.persistence.pymongo.pymongo_errors import (
    PyMongoOperationalDatabaseError,
    PyMongoInvalidCollectionNameError,
    PyMongoInvalidDatabaseNameError,
)
from petisco.persistence.pymongo.pymongo_persistence import PyMongoPersistence


@contextmanager
def get_mongo_collection(collection: str):
    client = PyMongoPersistence.get_instance().client
    database = PyMongoPersistence.get_instance().database
    try:
        db = client.get_database(database)
    except InvalidName as e:
        print(e)
        raise PyMongoInvalidDatabaseNameError(e)
    try:
        yield db.get_collection(collection)
    except InvalidName as e:
        print(e)
        raise PyMongoInvalidCollectionNameError(e)
    except PyMongoError as e:
        print(e)
        raise PyMongoOperationalDatabaseError(e)
