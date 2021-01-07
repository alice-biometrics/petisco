import concurrent.futures
import threading
from time import sleep

import pytest

from petisco import (
    SqliteDatabase,
    SqliteConnection,
    Persistence,
    SqlExecutor,
    MySqlConnection,
    MySqlDatabase,
    Uuid,
)
from petisco.fixtures import testing_with_mysql
from tests.modules.persistence.mother.model_filename_mother import ModelFilenameMother


@pytest.mark.integration
def test_should_sql_executor_with_sqlite_multithreading():
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

    def execute_sql_statement(name_thread):
        print(f"thread: {name_thread}")
        try:
            session_scope = Persistence.get_session_scope("sqlite_test")
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

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=number_of_threads
    ) as executor:
        for num_thread in range(number_of_threads):
            executor.submit(execute_sql_statement, num_thread)

    persistence.clear_data()
    persistence.delete()
    Persistence.clear()


@pytest.mark.integration
@testing_with_mysql
def test_should_sql_executor_with_mysql_multithreading():
    connection = MySqlConnection.create_local()
    filename = ModelFilenameMother.get("sql/persistence.sql.models.yml")

    database = MySqlDatabase(
        name="mysql_test",
        connection=connection,
        model_filename=filename,
        print_sql_statements=True,
    )

    persistence = Persistence()
    persistence.add(database)
    persistence.create()

    def execute_sql_statement(name_thread):
        print(f"thread: {name_thread}")
        print(threading.current_thread())

        try:
            session_scope = Persistence.get_session_scope("mysql_test")
            sql_executor = SqlExecutor(session_scope)

            uuid = Uuid.generate().value

            sql_executor.execute_statement(
                f'INSERT INTO Client (client_id,name) VALUES ("{uuid}","myclient")'
            )
            sql_executor.execute_statement(f"SELECT * FROM Client")
            sleep(1.0)
            # sql_executor.execute_statement(
            #     f'DELETE FROM Client WHERE client_id=\"{uuid}\";'
            # )
            return True
        except Exception as exp:
            print(exp)
            return False

    number_of_threads = 20

    # assert execute_sql_statement(1)

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

    # threads = {}
    # for num_thread in range(number_of_threads):
    #    threads[num_thread] = Thread(target=execute_sql_statement, args=(num_thread,))
    #    threads[num_thread].start()
    #
    # for num_thread in range(number_of_threads):
    #     assert threads[num_thread].join(), f"thread {num_thread} failed"

    # threads[0].join()

    persistence.clear_data()
    persistence.delete()
    Persistence.clear()
