import os

import pytest
from _pytest.logging import LogCaptureFixture
from meiga import AnyResult, Error, Failure, Success, early_return
from meiga.failures import WaitingForEarlyReturn
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Mapped, Session

from petisco.extra.sqlalchemy import SqlBase, SqlDatabase, SqliteConnection

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

ERROR = 40


class SqlUser(SqlBase):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(30))
    age: Mapped[int] = Column(Integer)


@pytest.mark.integration
class TestSqlDatabase:
    connection: SqliteConnection
    database: SqlDatabase

    def setup_method(self):
        self.connection = SqliteConnection.create(
            server_name="sqlite", database_name="petisco.db"
        )
        self.database: SqlDatabase = SqlDatabase(connection=self.connection)
        self.database.delete()

    def teardown_method(self):
        self.database.delete()

    def should_success_when_initialize(self):
        assert not self.database.is_available()
        self.database.initialize()
        assert self.database.is_available()

    def should_success_use_the_session_scope(self):
        self.database.initialize()
        session_scope = self.database.get_session_scope()

        with session_scope() as session:
            model = SqlUser(name="Petisco", age=3)
            session.add(model)

    def should_raise_a_connection_error_exception(self):
        with pytest.raises(ConnectionError):
            SqlDatabase(connection=None)

    def should_success_when_use_initial_statements_filename(self):
        database = SqlDatabase(
            connection=self.connection,
            initial_statements_filename=f"{ROOT_PATH}/initial_statements.sql",
        )
        database.initialize()
        session_scope = database.get_session_scope()

        with session_scope() as session:
            user_models = session.execute(select(SqlUser)).all()
            assert len(user_models) == 2

    def should_success_when_use_initial_statements_filename_and_before_and_after_callables(
        self,
    ):
        global before_spy
        global after_spy
        before_spy = False
        after_spy = False

        def before_statements() -> None:
            global before_spy
            before_spy = True

        def after_statements() -> None:
            global after_spy
            after_spy = True

        database = SqlDatabase(
            connection=self.connection,
            before_initial_statements=before_statements,
            initial_statements_filename=f"{ROOT_PATH}/initial_statements.sql",
            after_initial_statements=after_statements,
        )
        database.initialize()

        assert before_spy is True
        assert after_spy is True

        session_scope = database.get_session_scope()

        with session_scope() as session:
            user_models = session.execute(select(SqlUser)).all()
            assert len(user_models) == 2

    def should_fail_when_use_initial_statements_filename_with_invalid_filename(self):
        with pytest.raises(RuntimeError):
            database = SqlDatabase(
                connection=self.connection,
                initial_statements_filename="invalid_filename",
            )
            database.initialize()

    @pytest.mark.parametrize(
        "exception", [OperationalError(None, None, None), Exception()]
    )
    def should_log_rollback_and_raise_when_exceptions_are_raised(
        self, exception, caplog: LogCaptureFixture
    ):
        database = SqlDatabase(
            connection=self.connection,
            initial_statements_filename=f"{ROOT_PATH}/initial_statements.sql",
        )
        database.initialize()
        session_scope = database.get_session_scope()

        with pytest.raises(type(exception)):
            with session_scope() as session:  # noqa
                raise exception

        assert (
            "petisco.extra.sqlalchemy.sql.sql_session_scope_provider"
            == caplog.record_tuples[0][0]
        )
        assert ERROR == caplog.record_tuples[0][1]

    def should_rollback_and_raise_when_meiga_exception_is_raised(
        self, caplog: LogCaptureFixture
    ):
        database = SqlDatabase(
            connection=self.connection,
            initial_statements_filename=f"{ROOT_PATH}/initial_statements.sql",
        )
        database.initialize()
        session_scope = database.get_session_scope()

        with pytest.raises(WaitingForEarlyReturn):
            with session_scope() as session:  # noqa
                raise WaitingForEarlyReturn(None)

        assert len(caplog.record_tuples) == 0

    def should_session_deal_with_success_unwrap_or_return_style(self):
        database = SqlDatabase(
            connection=self.connection,
            initial_statements_filename=f"{ROOT_PATH}/initial_statements.sql",
        )
        database.initialize()
        session_scope = database.get_session_scope()

        def inner_function(session: Session) -> AnyResult:
            return Success(session.execute(select(SqlUser)).all())

        with session_scope() as session:
            user_models = inner_function(session).unwrap_or_return()
            assert len(user_models) == 2

    def should_session_deal_with_failure_unwrap_or_return_style(
        self, caplog: LogCaptureFixture
    ):
        database = SqlDatabase(
            connection=self.connection,
            initial_statements_filename=f"{ROOT_PATH}/initial_statements.sql",
        )
        database.initialize()
        session_scope = database.get_session_scope()

        class NotFoundError(Error):
            pass

        @early_return
        def main() -> AnyResult:
            def inner_function(session: Session) -> AnyResult:
                return Failure(NotFoundError())

            with session_scope() as session:
                inner_function(session).unwrap_or_return()

        result = main()
        result.assert_failure(value_is_instance_of=NotFoundError)

        assert len(caplog.record_tuples) == 0
