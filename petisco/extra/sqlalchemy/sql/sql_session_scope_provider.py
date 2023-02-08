from contextlib import contextmanager
from typing import Callable

from loguru import logger
from sqlalchemy.exc import OperationalError


def sql_session_scope_provider(Session) -> Callable:
    @contextmanager
    def session_scope():
        session = Session()
        try:
            yield session
            session.commit()
        except OperationalError as e:
            logger.error(e)
            session.rollback()
            raise e
        except Exception as e:
            logger.error(e)
            session.rollback()
            raise e
        finally:
            session.close()
        Session.remove()

    return session_scope
