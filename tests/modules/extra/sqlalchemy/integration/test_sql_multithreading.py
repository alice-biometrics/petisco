import concurrent.futures
from time import sleep

import pytest

from petisco import Uuid
from petisco.extra.sqlalchemy import (
    MySqlConnection,
    SqlDatabase,
    SqlExecutor,
    SqliteConnection,
)
from tests.modules.extra.decorators import testing_with_mysql


@pytest.mark.integration
class TestSqlMulithreading:
    def should_sql_executor_with_sqlite(self):
        connection = SqliteConnection.create(server_name="sqlite", database_name="petisco.db")
        database = SqlDatabase(connection=connection)
        database.initialize()

        def execute_sql_statement(name_thread):
            try:
                session_scope = database.get_session_scope()
                sql_executor = SqlExecutor(session_scope)

                sql_executor.execute_statement(
                    'INSERT INTO Client (client_id,name) VALUES ("65dd83ef-d315-417d-bfa8-1ab398e16f02","myclient")'
                )
                sql_executor.execute_statement(
                    'DELETE FROM Client WHERE client_id=="65dd83ef-d315-417d-bfa8-1ab398e16f02";'
                )
                return True
            except Exception as exp:
                print(exp)
                return False

        number_of_threads = 20

        with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_threads) as executor:
            for num_thread in range(number_of_threads):
                executor.submit(execute_sql_statement, num_thread)

        database.clear_data()

    @testing_with_mysql
    def should_sql_executor_with_mysql(self):
        connection = MySqlConnection.create_local()

        database = SqlDatabase(
            connection=connection,
            print_sql_statements=True,
        )
        database.initialize()

        def execute_sql_statement(name_thread):
            try:
                session_scope = database.get_session_scope()
                sql_executor = SqlExecutor(session_scope)

                uuid = Uuid.v4().value

                sql_executor.execute_statement(
                    f'INSERT INTO Client (client_id,name) VALUES ("{uuid}","myclient")'
                )
                sql_executor.execute_statement("SELECT * FROM Client")
                sleep(1.0)
                sql_executor.execute_statement(f'DELETE FROM Client WHERE client_id="{uuid}";')
                return True
            except Exception as exp:
                print(exp)
                return False

        number_of_threads = 20

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=number_of_threads, thread_name_prefix="sql_threads"
        ) as executor:
            future_to_sql = {
                executor.submit(execute_sql_statement, num_thread): num_thread
                for num_thread in range(number_of_threads)
            }
            for future in concurrent.futures.as_completed(future_to_sql):
                num_thread = future_to_sql[future]
                assert future.result(), f"thread {num_thread} failed"

        database.clear_data()
