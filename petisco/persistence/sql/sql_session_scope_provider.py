from contextlib import contextmanager
from typing import Callable

from sqlalchemy.exc import OperationalError

from petisco.persistence.sqlalchemy.sqlalchemy_operational_database_error import (
    SqlAlchemyOperationalDatabaseError,
)


def sql_session_scope_provider(session) -> Callable:
    @contextmanager
    def session_scope():
        try:
            yield session
            session.commit()
        except OperationalError as e:
            print(e)
            session.rollback()
            raise SqlAlchemyOperationalDatabaseError
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return session_scope
