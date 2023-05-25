import pytest

from petisco import Database, Databases
from petisco.base.domain.persistence.async_fake_database import AsyncFakeDatabase
from petisco.base.domain.persistence.fake_database import FakeDatabase


@pytest.mark.unit
class TestDatabases:
    @pytest.mark.parametrize(
        "database", [FakeDatabase(name="fake"), AsyncFakeDatabase(name="fake")]
    )
    def should_execute_lifecycle_of_persistence_with_fake_database(
        self, database: Database
    ):
        databases = Databases()
        databases.add(database)
        assert ["fake"] == databases.get_available_databases()

        info = databases.get_info()
        assert info == {"fake": {"name": "fake"}}
        assert str(databases) == "Databases: {'fake': {'name': 'fake'}}"

        databases.remove("fake")
        assert [] == databases.get_available_databases()

        assert Databases.info() == {}
        databases.initialize()
        databases.delete()
        Databases.clear()

    def should_check_if_are_not_available(self):
        Databases.clear()
        assert not Databases.are_available()

    @pytest.mark.asyncio
    async def should_async_check_if_are_not_available(self):
        Databases.clear()
        assert not await Databases.async_are_available()

    def should_check_not_exist_when_no_database_is_added(self):
        Databases.clear()
        assert not Databases.exist()
