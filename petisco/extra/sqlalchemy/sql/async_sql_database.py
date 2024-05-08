from __future__ import annotations

import re
from typing import AsyncContextManager, Callable, TypeVar

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session
from sqlalchemy_utils import database_exists

from petisco.base.domain.persistence.async_database import AsyncDatabase
from petisco.extra.sqlalchemy.sql.async_sql_session_scope_provider import (
    async_sql_session_scope_provider,
)
from petisco.extra.sqlalchemy.sql.sql_base import SqlBase
from petisco.extra.sqlalchemy.sql.sql_database import SqlDatabase

T = TypeVar("T")

AsyncSqlSessionScope = Callable[..., AsyncContextManager[AsyncSession]]


class AsyncSqlDatabase(SqlDatabase, AsyncDatabase[AsyncSession]):
    async_session_factory: async_sessionmaker | None = None

    async def initialize(self, base: DeclarativeBase = SqlBase) -> None:
        engine = create_async_engine(
            self.connection.url,
            json_serializer=lambda obj: obj,
            json_deserializer=lambda obj: obj,
            echo=self.print_sql_statements,
        )

        if not database_exists(engine.url):
            # await create_database(engine.url)
            async with engine.begin() as conn:
                await conn.run_sync(base.metadata.create_all)
                await self._async_run_initial_statements(conn)

        self.async_session_factory = async_sessionmaker(bind=engine)

    async def _async_run_initial_statements(self, conn) -> None:
        if self.initial_statements_filename:
            try:
                with open(self.initial_statements_filename) as file:
                    statements = re.split(r";\s*$", file.read(), flags=re.MULTILINE)
                for statement in statements:
                    if statement:
                        await conn.execute(text(statement))
            except Exception as exc:  # noqa
                raise RuntimeError(
                    f"Error loading the initial_statements_filename={self.initial_statements_filename}. {str(exc)}"
                ) from exc

    def get_session_scope(self) -> Callable[..., AsyncContextManager[AsyncSession]]:
        if self.async_session_factory is None:
            raise RuntimeError("AsyncSqlDatabase must run initialize() before get_session_scope()")

        if self.use_scoped_session:
            Session = scoped_session(self.async_session_factory)  # noqa
        else:
            Session = self.async_session_factory  # noqa
        return async_sql_session_scope_provider(Session)

    async def is_available(self) -> bool:
        try:
            context = self.get_session_scope()
            async with context() as session:
                await session.execute(text("SELECT 1"))
                _is_available = True
        except Exception:  # noqa E722
            _is_available = False
        return _is_available
