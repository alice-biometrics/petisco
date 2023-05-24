!!! note "" 
    
    The `SqlDatabase` is an specific implementation of a `Database` using a modern version of the SQLAlchemy ORM (version 2).
    This object encapsulates some specific SQLAlchemy stuff (e.g engine) and provides it as a scoped session to work with
    the defined models


## Connections

When you define a `SqlDatabase` you have to specify the connection. Petisco already provides connections to `MySQL` and
`SQLite`, but you can extend it with your requirements.

```python
from petisco.extra.sqlalchemy import MySqlConnection, SqlDatabase, SqliteConnection

...

if SQL_SERVER == "SQLite"
  connection = SqliteConnection.create("sqlite", "database.db") 
else:
  connection = MySqlConnection.from_environ() 

sql_database = SqlDatabase(name="petisco", connection=connection) 
```

## Models

To define your models, you have to inherit from `SqlBase` abstract object. Check the following example:

```python hl_lines="5"
from petisco import SqlBase
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped

class SqlUser(SqlBase):
    __tablename__ = "User"

    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(30))
    age: Mapped[int] = Column(Integer)
```

!!! help

    You can check the [`petisco-dev --sql-models`](../../../cli/#show-sql-models) cli tool to check which SQL models
    (inheriting from `SQLBase`) are available.

!!! warning 

    Only imported `SqlBase` models will be taken into account in caso of re-creation of all the tables. If you want to 
    create a table, but this model is no imported in your module. You can force importing it to bypass this problem.


```python hl_lines="7 8 9 12 20 21 22 23 24 25"
from petisco import SqlBase
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped


class User(BaseModel):
    name: str
    age: int | None


class SqlUser(SqlBase):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(30))
    age: Mapped[int] = Column(Integer)

    def to_domain(self) -> User:
        return User(name=self.name, age=self.age)

    @staticmethod
    def from_domain(domain_entity: User) -> "SQLUser":
        return SQLUser(name=domain_entity.name, age=domain_entity.age)
```


## Session

The `SQLDatabase` implements the `get_session_scope` method to get a context manager with a pre-configured 
`sqlalchemy.orm.Session`.

```python
session_scope = sql_database.get_session_scope()
with session_scope() as session:
    sql_user = SQLUser(name="Alice", age=3)
    session.add(sql_user)
```

To illustrate what is done in this context manager, you can check the session scope provider:

```python 
def sql_session_scope_provider(
    session_factory: Callable[[], Session]
) -> Callable[[], ContextManager[Session]]:
    @contextmanager
    def session_scope() -> ContextManager[Session]:
        session = session_factory()
        try:
            yield session
            session.commit()
        except OperationalError as e:
            logger.error(e)
            session.rollback()
            raise e
        except Exception as e:
            logger.error(e)
            session.rollback()
            raise e
        finally:
            session.close()
    return session_scope
```

Note that in this scope, session `commit` and `rollback` are taken into account to ease the way we develop, keeping the
security aspect.


## SqlExecutor

The `SqlExecutor` provides us a way to quickly execute SQL statements.

```python
from petisco.extra.sqlalchemy import SqlExecutor

session_scope = sql_database.get_session_scope()
sql_executor = SqlExecutor(session_scope)

# 1 SQL statmenet
sql_executor.execute_statement(
    'INSERT INTO User (name,age) VALUES ("Alice",3)'
)

# 2 SQL several statmenets
sql_executor.execute_statements(
    [
    'INSERT INTO User (name,age) VALUES ("Alice",3)',
    'INSERT INTO User (name,age) VALUES ("Bob",10)'
    ]
)

# 3 SQL statmenets from filename
sql_executor.execute_from_filename("insert_users.sql")
```

!!! tip

    When declare a `SqlDatabase` you can define a `initial_statements_filename` to run some SQL statements right after
    initialization.
    
    ```python hl_lines="4"
    sql_database = SqlDatabase(
        name="petisco", 
        connection=connection, 
        initial_statements_filename="sql_statements.sql"
    ) 
    ```

## Examples

### Sync

You can check the following example, and execute it with:

```bash
cd examples/persistence
python run_sql_database.py
```

```python title="examples/persistence/run_sql_database.py"
from __future__ import annotations

import os
from typing import TypeVar

from sqlalchemy import select

from petisco.extra.sqlalchemy import SqliteConnection, SqlDatabase
from examples.persistence.models.sql_user import SqlUser


T = TypeVar("T")

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASE_NAME = "my-database"
DATABASE_FILENAME = "sqlite.db"
SERVER_NAME = "sqlite"

sql_database = SqlDatabase(
    name=DATABASE_NAME,
    connection=SqliteConnection.create(SERVER_NAME, DATABASE_FILENAME),
)
sql_database.initialize()
session_scope = sql_database.get_session_scope()

with session_scope() as session:

    stmt = select(SqlUser)
    users = session.execute(stmt).all()
    print(f"{users=}")

    session.add(SqlUser(name="Alice", age="3"))
    session.add(SqlUser(name="Bob", age="10"))
    session.commit()

    stmt = select(SqlUser).where(SqlUser.name == "Alice")
    user = session.execute(stmt).first()
    print(user)

    stmt = select(SqlUser)
    users = session.execute(stmt).all()
    print(f"{users=}")
```

Where `examples/persistence/models/sql_user.py` is:

```python title="examples/persistence/models/sql_user.py"
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped

from petisco import SqlBase


class User(BaseModel):
    name: str
    age: int | None


class SqlUser(SqlBase):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(30))
    age: Mapped[int] = Column(Integer)

    def to_domain(self) -> User:
        return User(name=self.name, age=self.age)

    @staticmethod
    def from_domain(domain_entity: User) -> "SQLUser":
        return SqlUser(name=domain_entity.name, age=domain_entity.age)
```

### Async

Petisco also provides an async implementation, the `AsyncSqlDatabase`. To run it with async/await pattern, you could run
the following commands

```bash
cd examples/persistence
python run_async_sql_database.py
```

Where `examples/persistence/run_async_sql_database.py` is:

```python title="examples/persistence/run_async_sql_database.py"
import asyncio
import os

from sqlalchemy import select
from examples.persistence.models import SqlUser
from petisco.extra.sqlalchemy import AsyncSqlDatabase, SqliteConnection

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASE_NAME = "my-database"
DATABASE_FILENAME = "sqlite.db"
SERVER_NAME = "sqlite+aiosqlite"


async def main():
    sql_database = AsyncSqlDatabase(
        name=DATABASE_NAME,
        connection=SqliteConnection.create(SERVER_NAME, DATABASE_FILENAME),
    )
    await sql_database.initialize()
    session_scope = sql_database.get_session_scope()

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


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```



