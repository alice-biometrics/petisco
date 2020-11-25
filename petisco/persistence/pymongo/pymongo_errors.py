from petisco.domain.errors.critical_error import CriticalError


class PyMongoOperationalDatabaseError(CriticalError):
    pass


class PyMongoInvalidDatabaseNameError(CriticalError):
    def __init__(self, database: str):
        self.message = f"Invalid database name: {database}"


class PyMongoInvalidCollectionNameError(CriticalError):
    def __init__(self, collection: str):
        self.message = f"Invalid collection name: {collection}"
