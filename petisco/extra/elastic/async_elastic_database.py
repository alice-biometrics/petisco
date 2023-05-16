from typing import Any, Callable, List

from elasticsearch import AsyncElasticsearch

from petisco.base.domain.persistence.database import Database
from petisco.extra.elastic.async_elastic_session_scope_provider import (
    async_elastic_session_scope_provider,
)
from petisco.extra.elastic.elastic_connection import ElasticConnection


class AsyncElasticDatabase(Database):
    session: AsyncElasticsearch

    @staticmethod
    def local_connection_checker() -> "AsyncElasticDatabase":
        return AsyncElasticDatabase(
            name="test", connection=ElasticConnection.create_local()
        )

    def __init__(self, name: str, connection: ElasticConnection) -> None:
        if not connection or not isinstance(connection, ElasticConnection):
            raise ConnectionError(
                "ElasticDatabase needs a valid ElasticConnection connection"
            )
        self.connection = connection
        super().__init__(name)

    def create(self) -> None:
        from elasticsearch import AsyncElasticsearch

        self.session = AsyncElasticsearch(
            self.connection.to_elastic_format(), http_auth=self.connection.http_auth
        )

    def delete(self) -> None:
        pass

    def clear_data(self) -> None:
        pass

    async def is_available(self) -> bool:
        try:
            return await self.get_session().ping()
        except Exception:  # noqa E722
            return False

    def get_base(self) -> None:
        return None

    def get_model(self, model_name: str) -> Any:
        return None

    def get_model_names(self) -> List[str]:
        return []

    def get_session(self) -> AsyncElasticsearch:
        return self.session

    def get_session_scope(self) -> Callable:
        return async_elastic_session_scope_provider(self.get_session())
