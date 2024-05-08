from __future__ import annotations

import os
import re
from typing import Callable, ContextManager, TypeVar

from loguru import logger
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, scoped_session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from petisco.base.domain.persistence.database import Database
from petisco.extra.sqlalchemy.sql.mysql.mysql_connection import MySqlConnection
from petisco.extra.sqlalchemy.sql.sql_base import SqlBase
from petisco.extra.sqlalchemy.sql.sql_session_scope_provider import (
    sql_session_scope_provider,
)
from petisco.extra.sqlalchemy.sql.sqlite.sqlite_connection import SqliteConnection

T = TypeVar("T")

SqlSessionScope = Callable[..., ContextManager[Session]]


class SqlDatabase(Database[Session]):
    session_factory: sessionmaker | None = None

    def __init__(
        self,
        connection: SqliteConnection | MySqlConnection,
        *,
        alias: str | None = None,
        print_sql_statements: bool = False,
        use_scoped_session: bool = True,
        before_initial_statements: Callable[[], None] | None = None,
        initial_statements_filename: str | None = None,
        after_initial_statements: Callable[[], None] | None = None,
    ):
        self.connection = connection
        self.print_sql_statements = print_sql_statements
        self.use_scoped_session = use_scoped_session
        self.before_initial_statements = before_initial_statements
        self.initial_statements_filename = initial_statements_filename
        self.after_initial_statements = after_initial_statements
        self._check_connection()
        super().__init__(alias)

    def _check_connection(self) -> None:
        if not self.connection or not isinstance(self.connection, (SqliteConnection, MySqlConnection)):
            raise ConnectionError("SqlDatabase needs a valid SqliteConnection or MySqlConnection connection")

    def initialize(self, base: type[DeclarativeBase] = SqlBase) -> None:
        engine = create_engine(
            self.connection.url,
            pool_pre_ping=True,
            json_serializer=lambda obj: obj,
            json_deserializer=lambda obj: obj,
            echo=self.print_sql_statements,
        )

        if not database_exists(engine.url):
            create_database(engine.url)
            base.metadata.create_all(engine)
            if self.before_initial_statements:
                self.before_initial_statements()
            self._run_initial_statements(engine)
            if self.after_initial_statements:
                self.after_initial_statements()

        self.session_factory = sessionmaker(bind=engine)

    def _run_initial_statements(self, engine) -> None:
        if self.initial_statements_filename:
            try:
                with open(self.initial_statements_filename) as file:
                    statements = re.split(r";\s*$", file.read(), flags=re.MULTILINE)
                with engine.connect() as conn:
                    for statement in statements:
                        if statement:
                            conn.execute(text(statement))
                    conn.commit()
            except Exception as exc:  # noqa
                raise RuntimeError(
                    f"Error loading the initial_statements_filename={self.initial_statements_filename}. {str(exc)}"
                ) from exc

    def delete(self):
        if isinstance(self.connection, SqliteConnection):
            if os.path.exists(self.connection.database_name):
                os.remove(self.connection.database_name)
        else:
            logger.warning("SqlDatabase do not implement delete to mitigate possible problems in production")

    def clear_data(self, base: DeclarativeBase = SqlBase) -> None:
        if isinstance(self.connection, SqliteConnection):
            session_scope = self.get_session_scope()
            with session_scope() as session:
                for table in reversed(base.metadata.sorted_tables):
                    session.execute(table.delete())
        else:
            logger.warning(
                "SqlDatabase do not implement clear_data to mitigate possible problems in production"
            )

    def get_session_scope(self) -> Callable[..., ContextManager[Session]]:
        if self.session_factory is None:
            raise RuntimeError("SqlDatabase must run initialize() before get_session_scope()")

        if self.use_scoped_session:
            Session: Callable[..., Session] = scoped_session(self.session_factory)  # noqa
        else:
            Session: Callable[..., Session] = self.session_factory  # noqa
        return sql_session_scope_provider(Session)

    def is_available(self):
        try:
            context = self.get_session_scope()
            with context() as session:
                session.execute(text("SELECT 1"))
                _is_available = True
        except Exception:  # noqa E722
            _is_available = False
        return _is_available
