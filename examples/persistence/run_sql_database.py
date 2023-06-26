from __future__ import annotations

import os
from typing import TypeVar

from sqlalchemy import select

from examples.persistence.models.sql_user import SqlUser
from petisco import databases
from petisco.extra.sqlalchemy import SqlDatabase, SqliteConnection

T = TypeVar("T")

# Initialization
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASE_NAME = "my-database"
DATABASE_FILENAME = "sqlite.db"
SERVER_NAME = "sqlite"


def database_configurer() -> None:
    sql_database = SqlDatabase(
        alias=DATABASE_NAME,
        connection=SqliteConnection.create(SERVER_NAME, DATABASE_FILENAME),
    )
    databases.add(sql_database)
    databases.initialize()


def execution() -> None:
    session_scope = databases.get(SqlDatabase, alias=DATABASE_NAME).get_session_scope()

    with session_scope() as session:
        stmt = select(SqlUser)
        users = session.execute(stmt).all()
        print(f"{users=}")

        session.add(SqlUser(name="Alice", age="3"))
        session.add(SqlUser(name="Bob", age="10"))
        session.commit()

        stmt = select(SqlUser).where(SqlUser.name == "Alice")
        user = session.execute(stmt).fetchone()
        print(f"{user=}")

        stmt = select(SqlUser)
        users = session.execute(stmt).all()
        print(f"{users=}")


database_configurer()
execution()
