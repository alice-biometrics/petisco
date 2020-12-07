import pytest

from petisco import SqliteDatabase, SqliteConnection, Persistence
from tests.modules.persistence.mother.model_filename_mother import ModelFilenameMother


@pytest.mark.integration
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
    Persistence.clear()


@pytest.mark.integration
def test_should_add_an_user_with_sqlite_database_with_session():
    filename = ModelFilenameMother.get("sql/persistence.sql.models.yml")
    connection = SqliteConnection.create(
        server_name="sqlite", database_name="petisco.db"
    )
    database = SqliteDatabase(
        name="sqlite_test", connection=connection, model_filename=filename
    )

    persistence = Persistence()
    persistence.add(database)
    persistence.delete()
    persistence.create()

    UserModel = Persistence.get_model("sqlite_test", "user")

    session = Persistence.get_session("sqlite_test")
    model = UserModel(name="Petisco")
    session.add(model)
    session.commit()

    persistence.delete()
    Persistence.clear()


@pytest.mark.integration
def test_should_add_an_user_with_sqlite_database_with_session_scope():
    filename = ModelFilenameMother.get("sql/persistence.sql.models.yml")
    connection = SqliteConnection.create(
        server_name="sqlite", database_name="petisco.db"
    )
    database = SqliteDatabase(
        name="sqlite_test", connection=connection, model_filename=filename
    )

    persistence = Persistence()
    persistence.add(database)
    persistence.delete()
    persistence.create()

    UserModel = Persistence.get_model("sqlite_test", "user")
    with Persistence.get_session_scope("sqlite_test") as session:
        model = UserModel(name="Petisco")
        session.add(model)

    persistence.delete()
    Persistence.clear()
