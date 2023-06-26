import asyncio
import os

from sqlalchemy import select

from examples.persistence.models import SqlUser
from petisco import databases
from petisco.extra.sqlalchemy import AsyncSqlDatabase, SqliteConnection

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASE_NAME = "my-database"
DATABASE_FILENAME = "sqlite.db"
SERVER_NAME = "sqlite+aiosqlite"


async def database_configurer() -> None:
    sql_database = AsyncSqlDatabase(
        alias=DATABASE_NAME,
        connection=SqliteConnection.create(SERVER_NAME, DATABASE_FILENAME),
    )
    databases.add(sql_database)
    await databases.async_initialize()


async def execution() -> None:
    session_scope = databases.get(
        AsyncSqlDatabase, alias=DATABASE_NAME
    ).get_session_scope()

    async with session_scope() as session:
        stmt = select(SqlUser)
        users = (await session.execute(stmt)).all()
        print(f"{users=}")

        session.add(SqlUser(name="Alice", age="3"))
        session.add(SqlUser(name="Bob", age="10"))
        await session.commit()

        stmt = select(SqlUser).where(SqlUser.name == "Alice")
        user = (await session.execute(stmt)).first()
        print(user)

        stmt = select(SqlUser)
        users = (await session.execute(stmt)).all()
        print(f"{users=}")


async def main() -> None:
    await database_configurer()
    await execution()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
