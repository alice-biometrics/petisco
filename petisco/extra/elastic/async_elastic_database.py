from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Callable, ContextManager

from elasticsearch import AsyncElasticsearch
from loguru import logger

from petisco.base.domain.persistence.async_database import AsyncDatabase
from petisco.extra.elastic.elastic_connection import ElasticConnection


def async_elastic_session_scope_provider(session) -> Callable:
    from elasticsearch import RequestError

    @asynccontextmanager
    async def session_scope() -> ContextManager[AsyncElasticDatabase]:
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


AsyncElasticSessionScope = Callable[..., ContextManager[AsyncElasticsearch]]


class AsyncElasticDatabase(AsyncDatabase):
    session: AsyncElasticsearch | None = None

    @staticmethod
    def local_connection_checker(alias: str | None = "test") -> AsyncElasticDatabase:
        return AsyncElasticDatabase(alias=alias, connection=ElasticConnection.create_local())

    def __init__(self, alias: str, connection: ElasticConnection) -> None:
        if not connection or not isinstance(connection, ElasticConnection):
            raise ConnectionError("ElasticDatabase needs a valid ElasticConnection connection")
        self.connection = connection
        super().__init__(alias)

    def initialize(self) -> None:
        self.session = AsyncElasticsearch(
            self.connection.to_elastic_format(), http_auth=self.connection.http_auth
        )

    def delete(self) -> None:
        pass

    def clear_data(self) -> None:
        pass

    async def is_available(self) -> bool:
        try:
            return await self.session.ping()
        except Exception:  # noqa E722
            return False

    def get_session_scope(self) -> AsyncElasticSessionScope:
        return async_elastic_session_scope_provider(self.session)
