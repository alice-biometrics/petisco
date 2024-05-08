from contextlib import asynccontextmanager
from typing import AsyncContextManager, Callable

from loguru import logger
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession


def async_sql_session_scope_provider(
    async_session_factory: Callable[[], AsyncSession],
) -> Callable[..., AsyncContextManager[AsyncSession]]:
    @asynccontextmanager
    async def session_scope() -> AsyncContextManager[AsyncSession]:
        session = async_session_factory()
        try:
            yield session
            await session.commit()
        except OperationalError as e:
            logger.error(e)
            await session.rollback()
            raise e
        except Exception as e:
            logger.error(e)
            await session.rollback()
            raise e
        finally:
            await session.close()
        # await session.delete()

    return session_scope
