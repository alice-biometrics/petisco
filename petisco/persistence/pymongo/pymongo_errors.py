from meiga import Error


class PyMongoOperationalDatabaseError(Error):
    pass


class PyMongoInvalidDatabaseNameError(Error):
    def __init__(self, database: str):
        self.message = f"Invalid database name: {database}"


class PyMongoInvalidCollectionNameError(Error):
    def __init__(self, collection: str):
        self.message = f"Invalid collection name: {collection}"
