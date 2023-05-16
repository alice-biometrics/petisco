import pytest

from petisco import Persistence
from petisco.extra.elastic import ElasticConnection
from petisco.extra.elastic.async_elastic_database import AsyncElasticDatabase
from tests.modules.extra.decorators import testing_with_elastic


@pytest.mark.integration
@pytest.mark.asyncio
class TestAsyncElasticDatabase:
    @testing_with_elastic
    async def should_execute_a_session(self):
        connection = ElasticConnection.create_local()
        database = AsyncElasticDatabase(name="elastic_test", connection=connection)
        database.create()
        session_scope = database.get_session_scope()
        async with session_scope() as es:
            document = {
                "title": "Example Document",
                "content": "This is the content of the document.",
            }
            index_name = "my-index"
            response = await es.index(index=index_name, body=document)
            assert response.get("result") == "created"

    @testing_with_elastic
    async def should_create_persistence_with_elastic_database(self):
        connection = ElasticConnection.create_local()
        database = AsyncElasticDatabase(name="elastic_test", connection=connection)
        Persistence.clear()

        persistence = Persistence()
        persistence.add(database)

        assert database.info() == {"name": "elastic_test"}

        persistence.create()

        is_available = await Persistence.async_is_available(database.name)
        assert is_available is True

        persistence.delete()
        Persistence.clear()

    @testing_with_elastic
    async def should_create_persistence_with_elastic_database_specifying_the_database(
        self,
    ):
        connection = ElasticConnection.create_local()
        database = AsyncElasticDatabase(name="elastic_test", connection=connection)
        Persistence.clear()

        persistence = Persistence()
        persistence.add(database)

        assert database.info() == {"name": "elastic_test"}

        persistence.create()

        is_available = await Persistence.async_is_available(database.name)
        assert is_available is True

        persistence.delete()
        Persistence.clear()
