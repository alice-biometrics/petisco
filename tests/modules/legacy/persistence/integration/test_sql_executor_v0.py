import pytest

from petisco.legacy import SqliteDatabase, SqliteConnection, Persistence, SqlExecutor
from tests.modules.legacy.persistence.mother.model_filename_mother import (
    ModelFilenameMother,
)


@pytest.mark.integration
def test_should_sql_executor_insert_statement():
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

    session_scope = Persistence.get_session_scope("sqlite_test")
    sql_executor = SqlExecutor(session_scope)

    sql_executor.execute_statement(
        'INSERT INTO Client (client_id,name) VALUES ("65dd83ef-d315-417d-bfa8-1ab398e16f02","myclient")'
    )
    sql_executor.execute_statement(
        'DELETE FROM Client WHERE client_id="65dd83ef-d315-417d-bfa8-1ab398e16f02";'
    )

    persistence.clear_data()
    persistence.delete()
    Persistence.clear()


@pytest.mark.integration
def test_should_sql_executor_from_filename_with_statement():
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

    session_scope = Persistence.get_session_scope("sqlite_test")
    sql_executor = SqlExecutor(session_scope)

    sql_executor.execute_from_filename(
        "tests/modules/legacy/persistence/sql/client_create.sql"
    )
    sql_executor.execute_from_filename(
        "tests/modules/legacy/persistence/sql/client_delete.sql"
    )

    persistence.clear_data()
    persistence.delete()
    Persistence.clear()
