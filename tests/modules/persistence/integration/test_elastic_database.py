import pytest

from petisco import Persistence
from petisco.fixtures import testing_with_elastic
from petisco.persistence.elastic.elastic_connection import ElasticConnection
from petisco.persistence.elastic.elastic_database import ElasticDatabase


@pytest.mark.integration
@testing_with_elastic
def test_should_create_persistence_with_elastic_database():
    connection = ElasticConnection.create_local()
    database = ElasticDatabase(name="elastic_test", connection=connection)
    Persistence.clear()

    persistence = Persistence()
    persistence.add(database)

    assert database.info() == {"name": "elastic_test"}

    persistence.create()

    assert Persistence.is_available()

    persistence.delete()
    Persistence.clear()
