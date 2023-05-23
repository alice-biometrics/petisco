from __future__ import annotations

from typing import AsyncContextManager, Callable, TypeVar

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, scoped_session
from sqlalchemy_utils import create_database, database_exists

from petisco.base.domain.persistence.async_database import AsyncDatabase
from petisco.base.domain.persistence.sql_base import SqlBase
from petisco.extra.sqlalchemy.sql.async_sql_session_scope_provider import (
    async_sql_session_scope_provider,
)
from petisco.extra.sqlalchemy.sql.sql_database import SqlDatabase

T = TypeVar("T")


class AsyncSqlDatabase(SqlDatabase, AsyncDatabase[Session]):

    async_session_factory: async_sessionmaker | None = None

    async def initialize(self, base: DeclarativeBase = SqlBase) -> None:
        engine = create_async_engine(
            self.connection.url,
            json_serializer=lambda obj: obj,
            json_deserializer=lambda obj: obj,
            echo=self.print_sql_statements,
        )

        if not database_exists(engine.url):
            create_database(engine.url)
            async with engine.begin() as conn:
                await conn.run_sync(base.metadata.create_all)

        self.async_session_factory = async_sessionmaker(bind=engine)

    def get_session_scope(self) -> Callable[..., AsyncContextManager[T]]:
        if self.async_session_factory is None:
            raise RuntimeError(
                "AsyncSqlDatabase must run initialize() before get_session_scope()"
            )

        if self.use_scoped_session:
            Session = scoped_session(self.async_session_factory)  # noqa
        else:
            Session = self.async_session_factory  # noqa
        return async_sql_session_scope_provider(Session)

    async def is_available(self):
        try:
            context = self.get_session_scope()
            async with context() as session:
                await session.execute(text("SELECT 1"))
                _is_available = True
        except Exception:  # noqa E722
            _is_available = False
        return _is_available
