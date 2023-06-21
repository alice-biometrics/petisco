import os

import pytest
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import Mapped

from petisco import SqlBase
from petisco.extra.sqlalchemy import AsyncSqlDatabase, SqliteConnection

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


class SqlUser(SqlBase):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(30))
    age: Mapped[int] = Column(Integer)


@pytest.mark.asyncio
@pytest.mark.integration
class TestAsyncSqlDatabase:
    connection: SqliteConnection
    database: AsyncSqlDatabase

    def setup_method(self):
        self.connection = SqliteConnection.create(
            server_name="sqlite+aiosqlite", database_name="petisco.db"
        )
        self.database = AsyncSqlDatabase(connection=self.connection)

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
            AsyncSqlDatabase(connection=None)

    async def should_success_when_use_initial_statements_filename(self):
        database = AsyncSqlDatabase(
            connection=self.connection,
            initial_statements_filename=f"{ROOT_PATH}/initial_statements.sql",
        )
        await database.initialize()
        session_scope = database.get_session_scope()

        async with session_scope() as session:
            user_models = (await session.execute(select(SqlUser))).all()
            assert len(user_models) == 2

    async def should_fail_when_use_initial_statements_filename_with_invalid_filename(
        self,
    ):
        with pytest.raises(RuntimeError):
            database = AsyncSqlDatabase(
                connection=self.connection,
                initial_statements_filename="invalid_filename",
            )
            await database.initialize()
