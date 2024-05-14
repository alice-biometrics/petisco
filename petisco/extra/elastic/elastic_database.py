from __future__ import annotations

from contextlib import contextmanager
from typing import Callable, ContextManager

from elasticsearch import Elasticsearch
from loguru import logger

from petisco.base.domain.persistence.database import Database
from petisco.extra.elastic.elastic_connection import ElasticConnection


def elastic_session_scope_provider(
    session,
) -> Callable[..., ContextManager[Elasticsearch]]:
    from elasticsearch import RequestError

    @contextmanager
    def session_scope() -> ContextManager[Elasticsearch]:
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


ElasticSessionScope = Callable[..., ContextManager[Elasticsearch]]


class ElasticDatabase(Database):
    session: Elasticsearch | None = None

    @staticmethod
    def local_connection_checker(alias: str | None = "test") -> ElasticDatabase:
        return ElasticDatabase(alias=alias, connection=ElasticConnection.create_local())

    def __init__(self, alias: str, connection: ElasticConnection) -> None:
        if not connection or not isinstance(connection, ElasticConnection):
            raise ConnectionError("ElasticDatabase needs a valid ElasticConnection connection")
        self.connection = connection
        super().__init__(alias)

    def initialize(self) -> None:
        self.session = Elasticsearch(self.connection.to_elastic_format(), http_auth=self.connection.http_auth)

    def delete(self) -> None:
        pass

    def clear_data(self) -> None:
        pass

    def is_available(self) -> bool:
        try:
            return self.session.ping()
        except Exception:  # noqa E722
            return False

    def get_session_scope(self) -> ElasticSessionScope:
        return elastic_session_scope_provider(self.session)
