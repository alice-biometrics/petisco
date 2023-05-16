from contextlib import asynccontextmanager
from typing import Callable

from loguru import logger


def async_elastic_session_scope_provider(session) -> Callable:
    from elasticsearch import RequestError

    @asynccontextmanager
    async def session_scope():
        try:
            yield session
            await session.close()
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
