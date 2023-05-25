import pytest

from petisco import Databases
from petisco.extra.elastic import ElasticConnection, ElasticDatabase
from tests.modules.extra.decorators import testing_with_elastic


@pytest.mark.integration
class TestElasticDatabase:
    @testing_with_elastic
    def should_execute_a_session(self):
        connection = ElasticConnection.create_local()
        database = ElasticDatabase(name="elastic_test", connection=connection)
        database.initialize()

        session_scope = database.get_session_scope()

        with session_scope() as es:
            document = {
                "title": "Example Document",
                "content": "This is the content of the document.",
            }
            index_name = "my-index"
            response = es.index(index=index_name, document=document)
            assert response.get("result") == "created"

    @testing_with_elastic
    def should_create_databases_with_elastic_database(self):
        connection = ElasticConnection.create_local()
        database = ElasticDatabase(name="elastic_test", connection=connection)
        Databases.clear()

        databases = Databases()
        databases.add(database)

        assert database.info() == {"name": "elastic_test"}

        databases.initialize()

        assert Databases.are_available()

        databases.delete()
        Databases.clear()

    @testing_with_elastic
    def should_create_persistence_with_elastic_database_specifying_the_database(self):
        connection = ElasticConnection.create_local()
        database = ElasticDatabase(name="elastic_test", connection=connection)
        Databases.clear()

        databases = Databases()
        databases.add(database)

        assert database.info() == {"name": "elastic_test"}

        databases.initialize()

        assert Databases.are_available(database.name)

        databases.delete()
        Databases.clear()
