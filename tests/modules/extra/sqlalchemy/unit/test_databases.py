import pytest

from petisco import Database, databases
from petisco.base.domain.persistence.async_fake_database import AsyncFakeDatabase
from petisco.base.domain.persistence.fake_database import FakeDatabase


@pytest.mark.unit
class TestDatabases:
    def setup_method(self):  # noqa
        databases.clear()

    def teadown_method(self):  # noqa
        databases.clear()

    @pytest.mark.parametrize("database", [FakeDatabase(), AsyncFakeDatabase()])
    def should_execute_lifecycle_of_persistence_with_fake_database(
        self, database: Database
    ):
        classname = database.__class__.__name__
        assert [] == databases.get_database_names()

        databases.add(database)
        assert [classname] == databases.get_database_names()

        assert databases.info() == {classname: {"alias": None, "type": classname}}

        databases.remove(type(database))
        assert [] == databases.get_database_names()

        assert databases.info() == {}
        databases.initialize()
        databases.delete()

    def should_add_databases_with_two_alias(self):
        database_1 = FakeDatabase(alias="database_1")
        database_2 = FakeDatabase(alias="database_2")

        databases.add([database_1, database_2])

        assert ["database_1", "database_2"] == databases.get_database_names()

        retrieved_database_1 = databases.get(FakeDatabase, alias="database_1")
        retrieved_database_2 = databases.get(FakeDatabase, alias="database_2")

        assert retrieved_database_1 == database_1
        assert retrieved_database_2 == database_2

        databases.remove(FakeDatabase, alias="database_1")
        databases.remove(FakeDatabase, alias="database_2")

        assert [] == databases.get_database_names()
