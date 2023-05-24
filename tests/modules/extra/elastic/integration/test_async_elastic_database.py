import pytest

from petisco import Databases
from petisco.extra.elastic import AsyncElasticDatabase, ElasticConnection
from tests.modules.extra.decorators import testing_with_elastic


@pytest.mark.asyncio
@pytest.mark.integration
class TestAsyncElasticDatabase:
    @testing_with_elastic
    async def should_execute_a_session(self):
        connection = ElasticConnection.create_local()
        database = AsyncElasticDatabase(name="elastic_test", connection=connection)
        database.initialize()

        session_scope = database.get_session_scope()

        async with session_scope() as es:
            document = {
                "title": "Example Document",
                "content": "This is the content of the document.",
            }
            index_name = "my-index"
            response = await es.index(index=index_name, document=document)
            assert response.get("result") == "created"

    @testing_with_elastic
    async def should_create_databases_with_elastic_database(self):
        connection = ElasticConnection.create_local()
        database = AsyncElasticDatabase(name="elastic_test", connection=connection)
        Databases.clear()

        databases = Databases()
        databases.add(database)

        assert database.info() == {"name": "elastic_test"}

        databases.initialize()

        assert await Databases.async_are_available()

        databases.delete()
        Databases.clear()

    @testing_with_elastic
    async def should_create_persistence_with_elastic_database_specifying_the_database(
        self,
    ):
        connection = ElasticConnection.create_local()
        database = AsyncElasticDatabase(name="elastic_test", connection=connection)
        Databases.clear()

        databases = Databases()
        databases.add(database)

        assert database.info() == {"name": "elastic_test"}

        databases.initialize()

        assert await Databases.async_are_available(database.name)

        databases.delete()
        Databases.clear()
