from contextlib import contextmanager
from typing import Callable

from loguru import logger


def elastic_session_scope_provider(session) -> Callable:
    from elasticsearch import RequestError

    @contextmanager
    def session_scope():
        try:
            yield session
        except ConnectionRefusedError as e:
            logger.error(e)
            raise e
        except RequestError as e:
            logger.error(e)
            raise e
        except Exception as e:
            logger.error(e)
            raise e

    return session_scope
