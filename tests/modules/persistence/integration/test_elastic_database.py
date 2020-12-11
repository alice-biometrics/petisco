import pytest

from petisco import Persistence
from petisco.persistence.elastic.elastic_connection import ElasticConnection
from petisco.persistence.elastic.elastic_database import ElasticDatabase
from petisco.persistence.elastic.elastic_is_running_locally import (
    elastic_is_running_locally,
)


@pytest.mark.integration
@pytest.mark.skipif(
    not elastic_is_running_locally(), reason="Elastic is not running locally"
)
def test_should_create_persistence_with_elastic_database():
    connection = ElasticConnection.create_local()
    database = ElasticDatabase(name="elastic_test", connection=connection)

    persistence = Persistence()
    persistence.add(database)
    persistence.create()
    persistence.delete()
    Persistence.clear()
