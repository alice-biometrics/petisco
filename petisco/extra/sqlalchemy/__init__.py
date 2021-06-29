from petisco.extra.sqlalchemy.is_sqlalchemy_available import is_sqlalchemy_available

sqlalchemy = []
if is_sqlalchemy_available():
    from petisco.extra.sqlalchemy.sql.mysql.mysql_connection import MySqlConnection
    from petisco.extra.sqlalchemy.sql.mysql.mysql_database import MySqlDatabase
    from petisco.extra.sqlalchemy.sql.sqlite.sqlite_connection import SqliteConnection
    from petisco.extra.sqlalchemy.sql.sqlite.sqlite_database import SqliteDatabase
    from petisco.extra.sqlalchemy.sql.sql_executor import SqlExecutor

    sqlalchemy = [
        "MySqlConnection",
        "MySqlDatabase",
        "SqliteConnection",
        "SqliteDatabase",
        "SqlExecutor",
    ]
else:
    sqlalchemy = []

__all__ = sqlalchemy
