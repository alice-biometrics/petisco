import pytest

from petisco import Persistence
from petisco.extra.sqlalchemy import LegacySqliteDatabase, SqliteConnection
from tests.modules.extra.sqlalchemy.mother.model_filename_mother import (
    ModelFilenameMother,
)


@pytest.mark.skip
@pytest.mark.integration
def test_should_create_persistence_with_legacy_sqlite_database():
    filename = ModelFilenameMother.get("sql/persistence.sql.models.yml")
    connection = SqliteConnection.create(
        server_name="sqlite", database_name="petisco.db"
    )
    database = LegacySqliteDatabase(
        name="sqlite_test", connection=connection, model_filename=filename
    )

    persistence = Persistence()
    persistence.add(database)
    persistence.create()

    assert database.info() == {
        "name": "sqlite_test",
        "models": {
            "client": "tests.modules.extra.sqlalchemy.ymls.sql.models.ClientModel",
            "product": "tests.modules.extra.sqlalchemy.ymls.sql.models.ProductModel",
            "user": "tests.modules.extra.sqlalchemy.ymls.sql.models.UserModel",
        },
    }
    assert Persistence.is_available()

    persistence.delete()
    Persistence.clear()


@pytest.mark.skip
@pytest.mark.integration
def test_should_add_an_user_with_legacy_sqlite_database_with_session():
    filename = ModelFilenameMother.get("sql/persistence.sql.models.yml")
    connection = SqliteConnection.create(
        server_name="sqlite", database_name="petisco.db"
    )
    database = LegacySqliteDatabase(
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


@pytest.mark.skip
@pytest.mark.integration
def test_should_add_a_product_with_legacy_sqlite_database_with_session_scope():
    filename = ModelFilenameMother.get("sql/persistence.sql.models.yml")
    connection = SqliteConnection.create(
        server_name="sqlite", database_name="petisco.db"
    )
    database = LegacySqliteDatabase(
        name="sqlite_test", connection=connection, model_filename=filename
    )

    persistence = Persistence()
    persistence.add(database)
    persistence.delete()
    persistence.create()

    ProductModel = Persistence.get_model("sqlite_test", "product")
    session_scope = Persistence.get_session_scope("sqlite_test")
    with session_scope() as session:
        model = ProductModel(name="Petisco", price=2)
        session.add(model)

    persistence.clear_data()
    persistence.delete()
    Persistence.clear()


@pytest.mark.skip
@pytest.mark.integration
def test_should_raise_a_connection_error_exception():
    filename = ModelFilenameMother.get("sql/persistence.sql.models.yml")

    with pytest.raises(ConnectionError):
        LegacySqliteDatabase(
            name="sqlite_test", connection=None, model_filename=filename
        )


@pytest.mark.skip
@pytest.mark.integration
def test_should_create_persistence_with_sqlite_database_without_filename():
    connection = SqliteConnection.create(
        server_name="sqlite", database_name="petisco.db"
    )
    database = LegacySqliteDatabase(
        name="sqlite_test", connection=connection, model_filename=None
    )

    persistence = Persistence()
    persistence.add(database)
    persistence.create()

    assert database.info() == {"name": "sqlite_test"}
    assert Persistence.is_available()

    persistence.delete()
    Persistence.clear()
