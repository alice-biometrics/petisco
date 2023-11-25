from contextlib import contextmanager
from typing import Callable, ContextManager, Iterator

import meiga
from loguru import logger
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

if meiga.__version__ < "1.9.4":
    from meiga.on_failure_exception import OnFailureException as WaitingForEarlyReturn
else:
    from meiga.failures import WaitingForEarlyReturn


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
