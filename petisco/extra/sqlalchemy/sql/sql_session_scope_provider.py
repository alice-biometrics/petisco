from contextlib import contextmanager
from typing import Callable, ContextManager, Iterator

from loguru import logger
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from petisco.extra.meiga import WaitingForEarlyReturn


def sql_session_scope_provider(
    session_factory: Callable[[], Session]
) -> Callable[[], ContextManager[Session]]:
    @contextmanager
    def session_scope() -> Iterator[Session]:
        session = session_factory()
        try:
            yield session
            session.commit()
        except OperationalError as e:
            logger.error(e)
            session.rollback()
            raise e
        except WaitingForEarlyReturn as e:
            session.rollback()
            raise e
        except Exception as e:
            logger.error(e)
            session.rollback()
            raise e
        finally:
            session.close()
        # session.delete()

    return session_scope
