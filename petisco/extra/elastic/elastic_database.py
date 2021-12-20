from typing import Callable, List

from petisco.base.domain.persistence.interface_database import Database
from petisco.extra.elastic.elastic_connection import ElasticConnection
from petisco.extra.elastic.elastic_session_scope_provider import (
    elastic_session_scope_provider,
)


class ElasticDatabase(Database):
    @staticmethod
    def local_connection_checker():
        return ElasticDatabase(name="test", connection=ElasticConnection.create_local())

    def __init__(self, name: str, connection: ElasticConnection):
        if not connection or not isinstance(connection, ElasticConnection):
            raise ConnectionError(
                "ElasticDatabase needs a valid ElasticConnection connection"
            )
        self.connection = connection
        super().__init__(name)

    def create(self):
        from elasticsearch import Elasticsearch

        self.session = Elasticsearch(
            self.connection.to_elastic_format(), http_auth=self.connection.http_auth
        )

    def delete(self):
        pass

    def clear_data(self):
        pass

    def is_available(self):
        try:
            return self.get_session().ping()
        except Exception:  # noqa E722
            return False

    def get_base(self):
        return None

    def get_model(self, model_name: str):
        return None

    def get_model_names(self) -> List[str]:
        return None

    def get_session(self):
        return self.session

    def get_session_scope(self) -> Callable:
        return elastic_session_scope_provider(self.get_session())
