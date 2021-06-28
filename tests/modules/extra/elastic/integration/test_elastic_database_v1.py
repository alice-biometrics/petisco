import pytest

from petisco.base.domain.persistence.persistence import Persistence
from petisco.extra.elastic.elastic_connection import ElasticConnection
from petisco.extra.elastic.elastic_database import ElasticDatabase
from tests.modules.extra.decorators import testing_with_elastic


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


@pytest.mark.integration
@testing_with_elastic
def test_should_create_persistence_with_elastic_database_specifying_the_database():
    connection = ElasticConnection.create_local()
    database = ElasticDatabase(name="elastic_test", connection=connection)
    Persistence.clear()

    persistence = Persistence()
    persistence.add(database)

    assert database.info() == {"name": "elastic_test"}

    persistence.create()

    assert Persistence.is_available(database.name)

    persistence.delete()
    Persistence.clear()
