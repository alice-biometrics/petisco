import pytest

from petisco.extra.sqlalchemy import SqlDatabase, SqlExecutor, SqliteConnection


@pytest.mark.integration
class TestSqlExecutor:
    database: SqlDatabase

    def setup_method(self):
        connection = SqliteConnection.create(
            server_name="sqlite", database_name="petisco.db"
        )
        self.database = SqlDatabase(connection=connection)
        self.database.initialize()

    def should_insert_statement(self):
        session_scope = self.database.get_session_scope()
        sql_executor = SqlExecutor(session_scope)

        sql_executor.execute_statement(
            'INSERT INTO Client (client_id,name) VALUES ("65dd83ef-d315-417d-bfa8-1ab398e16f02","myclient")'
        )
        sql_executor.execute_statement(
            'DELETE FROM Client WHERE client_id="65dd83ef-d315-417d-bfa8-1ab398e16f02";'
        )

    def should_from_filename_with_statement(self):
        session_scope = self.database.get_session_scope()
        sql_executor = SqlExecutor(session_scope)

        sql_executor.execute_from_filename(
            "tests/modules/extra/sqlalchemy/sql/client_create.sql"
        )
        sql_executor.execute_from_filename(
            "tests/modules/extra/sqlalchemy/sql/client_delete.sql"
        )
