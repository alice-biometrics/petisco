import pytest

from petisco import Databases, Persistence
from petisco.base.domain.persistence.fake_database import FakeDatabase


@pytest.mark.unit
class TestDatabases:
    def should_execute_lifecycle_of_persistence_with_fake_database(self):
        database = FakeDatabase(name="fake")

        databases = Databases()
        databases.add(database)
        assert ["fake"] == databases.get_available_databases()

        info = databases.get_info()
        assert info == {
            "fake": {
                "name": "fake",
            }
        }
        assert str(databases) == "Databases: {'fake': {'name': 'fake'}}"

        databases.remove("fake")
        assert [] == databases.get_available_databases()

        assert Databases.info() == {}
        databases.initialize()
        databases.delete()
        Databases.clear()

    def should_persistence_not_available_when_no_database_is_added(self):
        Persistence.clear()
        assert not Persistence.is_available()

    def should_persistence_not_exist_when_no_database_is_added(self):
        Persistence.clear()
        assert not Persistence.exist()
