from contextlib import contextmanager
from typing import Callable, ContextManager, Iterator

from loguru import logger
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from petisco.extra.meiga import WaitingForEarlyReturn


def sql_session_scope_provider(
    session_factory: Callable[[], Session],
) -> Callable[[], ContextManager[Session]]:
    @contextmanager
    def session_scope() -> Iterator[Session]:
        session = session_factory()
        try:
            yield session
            session.commit()
        except WaitingForEarlyReturn as e:
            session.rollback()
            raise e
        except (OperationalError, Exception) as e:
            logger.error(e)
            session.rollback()
            raise e
        finally:
            session.close()

    return session_scope
