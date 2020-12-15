from contextlib import contextmanager
from typing import Callable

from petisco.persistence.elastic.elastic_operational_database_error import (
    ElasticOperationalDatabaseError,
)


def elastic_session_scope_provider(session) -> Callable:
    from elasticsearch import RequestError

    @contextmanager
    def session_scope():
        try:
            yield session
        except ConnectionRefusedError:
            raise ElasticOperationalDatabaseError
        except RequestError as e:  # noqa E722
            raise ElasticOperationalDatabaseError
        except:  # noqa E722
            raise ElasticOperationalDatabaseError

    return session_scope
