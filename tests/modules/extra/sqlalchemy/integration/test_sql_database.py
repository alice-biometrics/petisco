import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped

from petisco import SqlBase
from petisco.extra.sqlalchemy import SqlDatabase, SqliteConnection


class SqlUser(SqlBase):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(30))
    age: Mapped[int] = Column(Integer)


@pytest.mark.integration
class TestSqlDatabase:
    database: SqlDatabase

    def setup_method(self):
        connection = SqliteConnection.create(
            server_name="sqlite", database_name="petisco.db"
        )
        self.database = SqlDatabase(name="sqlite_test", connection=connection)
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
            SqlDatabase(name="sqlite_test", connection=None)
