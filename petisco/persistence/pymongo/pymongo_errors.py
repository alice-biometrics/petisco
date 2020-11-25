from petisco.domain.errors.critical_error import CriticalError


class PyMongoOperationalDatabaseError(CriticalError):
    pass


class PyMongoInvalidDatabaseNameError(CriticalError):
    pass


class PyMongoInvalidCollectionNameError(CriticalError):
    pass
