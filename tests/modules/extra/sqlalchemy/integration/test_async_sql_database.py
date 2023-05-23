import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped

from petisco import SqlBase
from petisco.extra.sqlalchemy import AsyncSqlDatabase, SqliteConnection


class SqlUser(SqlBase):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(30))
    age: Mapped[int] = Column(Integer)


@pytest.mark.asyncio
@pytest.mark.integration
class TestAsyncSqlDatabase:
    database: AsyncSqlDatabase

    def setup_method(self):
        connection = SqliteConnection.create(
            server_name="sqlite+aiosqlite", database_name="petisco.db"
        )
        self.database = AsyncSqlDatabase(name="sqlite_test", connection=connection)

    def teardown_method(self):
        self.database.delete()

    async def should_success_when_initialize(self):
        assert not await self.database.is_available()
        await self.database.initialize()
        assert await self.database.is_available()

    async def should_success_use_the_session_scope(self):
        await self.database.initialize()
        session_scope = self.database.get_session_scope()

        async with session_scope() as session:
            model = SqlUser(name="Petisco", age=3)
            session.add(model)

    async def should_raise_a_connection_error_exception(self):
        with pytest.raises(ConnectionError):
            AsyncSqlDatabase(name="sqlite_test", connection=None)
