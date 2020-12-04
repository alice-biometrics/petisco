import pytest

from petisco import SqliteDatabase, SqliteConnection, Persistence
from tests.modules.persistence.mother.model_filename_mother import ModelFilenameMother


@pytest.mark.unit
def test_should_create_persistence_with_sqlite_database():
    filename = ModelFilenameMother.get("sql/persistence.sql.models.yml")
    connection = SqliteConnection.create(
        server_name="sqlite", database_name="petisco.db"
    )
    database = SqliteDatabase(
        name="sqlite_test", connection=connection, model_filename=filename
    )

    persistence = Persistence()
    persistence.add(database)
    persistence.create()
    persistence.delete()
