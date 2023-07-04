!!! note ""

    Petisco provides a high-level, intuitive, and Pythonic interface to interact with databases. It abstracts away the 
    complexities of working with different database systems, allowing developers to focus on their application logic rather 
    than the intricacies of various SQL dialects or low-level database operations. With this framework, you can work with 
    popular databases like MySQL, PostgreSQL, SQLite, Elastic, and many more, without having to learn the specifics of each 
    system.

## Configuration

We recommend to configure (and initialize) databases using an `ApplicationConfigurer`. Check the following example of a
`FastApiApplication`. 


```python hl_lines="13 21" title="app/application.py"
from petisco.extra.fastapi import FastApiApplication

from app import (
    APPLICATION_LATEST_DEPLOY,
    APPLICATION_NAME,
    APPLICATION_VERSION,
    ORGANIZATION,
)
from app.fastapi import fastapi_configurer
from app.petisco.dependencies.dependencies_provider import dependencies_provider
from app.petisco.configurers import DatabasesConfigurer

configurers = [DatabasesConfigurer()]

application = FastApiApplication(
    name=APPLICATION_NAME,
    version=APPLICATION_VERSION,
    organization=ORGANIZATION,
    deployed_at=APPLICATION_LATEST_DEPLOY,
    dependencies_provider=dependencies_provider,
    configurers=configurers,
    fastapi_configurer=fastapi_configurer,
)
```

In the `DatabasesConfigurer` we have to initialize databases, using the global `databases` object adding each 
implementation of `Database` abstract class. The following example configures a `SqlDatabase` connecting with a MySQL
or a SQLite backend depending on some configuration.

```python hl_lines="21 22 23"
import os

from petisco import ApplicationConfigurer, databases
from petisco.extra.sqlalchemy import MySqlConnection, SqlDatabase, SqliteConnection

DATABASE_NAME = "petisco-sql"
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
SQL_SERVER = os.getenv("SQL_SERVER", "sqlite")

class DatabasesConfigurer(ApplicationConfigurer):
    def execute(self, testing: bool = True) -> None:
        if testing or (SQL_SERVER == "sqlite"):
          test_db_filename = "onboarding-test.db"
          connection = SqliteConnection.create("sqlite", test_db_filename) 
        else:
          connection = MySqlConnection.from_environ() 

        sql_database = SqlDatabase(name=DATABASE_NAME, connection=connection) 
    
        databases.add(sql_database) # (1)
        databases.initialize() # (2)
```

1. Adds the `SqlDatabase` implementation to the global `databases` object
2. Initializes all the added implementations.

!!! tip "Use available implementations"
  
    Add other available implementation as `ElasticDatabase` easily with:
  
    ```petisco hl_lines="2 7 11"
      from petisco import databases
      from petisco.extra.elastic import ElasticDatabase, ElasticConnection
    
      ...
    
      sql_database = SqlDatabase(name=DATABASE_NAME, connection=connection) 
      elastic_database = ElasticDatabase(connection=ElasticConnection.create_local())
  
      databases.add(sql_database)
      databases.add(elastic_database)
      databases.initialize()
    ```

!!! tip "Extend Database"

    You can extend the `Database` abstract class and create your own implementation

    ```python
    from typing import Callable, ContextManager
    from petisco import Database
    
    class YourExtensionDatabase(Database):
 
        def initialize(self) -> None:
            # Add your stuff
            pass

        def delete(self):
            # Add your stuff
            pass
    
        def clear_data(self, base: DeclarativeBase = SqlBase) -> None:
            # Add your stuff
            pass
    
        def get_session_scope(self) -> Callable[..., ContextManager[T]]:
            # Add your stuff
            pass
    
        def is_available(self):
            # Add your stuff
            pass
    ```


## Usage 

Once databases are initialized (after `databases.initializes()`), we should be ready to use these implementations. 
Let's overview how to use it through a repository implementation. Note that uses `databases` instance to retrieve the 
`get_session_scope` for the specified database name.

```python hl_lines="9 10 11 12"
from meiga import BoolResult, early_return, isSuccess
from petisco import databases, Repository
from app.src.models import SqlUser, User


class SqlUserRepository(Repository):
    session_scope: SqlSessionScope

    def __init__(self):
        # `DATABASE_NAME = "petisco-sql"` -> same as defined in the configuration 
        database = databases.get(SqlDatabase, alias=DATABASE_NAME)
        self.session_scope = database.get_session_scope()

    @early_return
    def save(self, user: User) -> BoolResult:
        with self.session_scope() as session:
            sql_user = SqlUser.from_domain(user)
            session.add(sql_user)
        return isSuccess
    ...
```

If you inherit from `SqlRepository` or `ElasticRepository` you don't need to define the session scope and the 
`__init__` constructor:

```python hl_lines="6 17 18"
from meiga import BoolResult, early_return, isSuccess
from petisco.extra.sqlalchemy import SqlRepository
from app.src.models import SqlUser, User


class SqlUserRepository(SqlRepository):

    @early_return
    def save(self, user: User) -> BoolResult:
        with self.session_scope() as session:
            sql_user = SqlUser.from_domain(user)
            session.add(sql_user)
        return isSuccess
    ...


# `DATABASE_NAME = "petisco-sql"` -> same as defined in the configuration 
sql_user_repository = SqlUserRepository(database_alias=DATABASE_NAME)
```




!!! note

    For more details about how to use specific `Database` implementations, check the documentation in:

    * [SQLAlchemy](../extra/sqlalchemy/sqlalchemy/)
    * [Elastic](../extra/elastic/elastic/)

    Note both extra modules implements aync version since petisco v2!

