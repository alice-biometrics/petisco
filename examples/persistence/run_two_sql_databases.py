from __future__ import annotations

import os

from sqlalchemy import select

from examples.persistence.models.sql_profession import AlternativeSqlBase, SqlProfession
from examples.persistence.models.sql_user import SqlUser
from petisco import databases
from petisco.extra.sqlalchemy import SqlDatabase, SqliteConnection

# Initialization
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASE_NAME_1 = "my-database-1"
DATABASE_FILENAME_1 = "sqlite_1.db"
DATABASE_NAME_2 = "my-database-2"
DATABASE_FILENAME_2 = "sqlite_2.db"

SERVER_NAME = "sqlite"


def databases_configurer() -> None:
    sql_database_1 = SqlDatabase(
        alias=DATABASE_NAME_1,
        connection=SqliteConnection.create(SERVER_NAME, DATABASE_FILENAME_1),
    )
    sql_database_2 = SqlDatabase(
        alias=DATABASE_NAME_2,
        connection=SqliteConnection.create(SERVER_NAME, DATABASE_FILENAME_2),
    )
    databases.add(sql_database_1)
    databases.add(sql_database_2)

    databases.initialize(
        initialization_arguments={DATABASE_NAME_2: {"base": AlternativeSqlBase}}
    )


def execution() -> None:
    session_scope_1 = databases.get(
        SqlDatabase, alias=DATABASE_NAME_1
    ).get_session_scope()

    with session_scope_1() as session:
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

    session_scope_2 = databases.get(
        SqlDatabase, alias=DATABASE_NAME_2
    ).get_session_scope()

    with session_scope_2() as session:
        stmt = select(SqlProfession)
        professions = session.execute(stmt).all()
        print(f"{professions=}")

        session.add(SqlProfession(name="Alice", salary="1000"))
        session.add(SqlProfession(name="Bob", salary="2000"))
        session.commit()

        stmt = select(SqlProfession).where(SqlProfession.name == "Alice")
        profession = session.execute(stmt).fetchone()
        print(f"{profession=}")

        stmt = select(SqlProfession)
        professions = session.execute(stmt).all()
        print(f"{professions=}")


databases_configurer()
execution()
