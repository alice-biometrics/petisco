from contextlib import contextmanager
from sqlalchemy.exc import OperationalError

from petisco.persistence.sqlalchemy.sqlalchemy_operational_database_error import (
    SqlAlchemyOperationalDatabaseError,
)
from petisco.persistence.sqlalchemy.sqlalchemy_persistence import SqlAlchemyPersistence


@contextmanager
def session_scope(source: str):
    """Provide a transactional scope around a series of operations."""
    transactional_scope = SqlAlchemyPersistence.get_instance().sources[source][
        "session"
    ]()
    try:
        yield transactional_scope
        transactional_scope.commit()
    except OperationalError as e:
        print(e)
        transactional_scope.rollback()
        raise SqlAlchemyOperationalDatabaseError
    except Exception as e:
        transactional_scope.rollback()
        raise e
    finally:
        transactional_scope.close()
