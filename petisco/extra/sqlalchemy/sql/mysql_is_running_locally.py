from petisco.base.domain.persistence.databases import databases
from petisco.extra.sqlalchemy.sql.mysql.mysql_connection import MySqlConnection


def mysql_is_running_locally() -> bool:
    try:
        from petisco.extra.sqlalchemy.sql.sql_database import SqlDatabase

        database = SqlDatabase(connection=MySqlConnection.create_local())
        databases.add(database)
        databases.initialize()
        is_running_locally = True
    except:  # noqa: E722
        is_running_locally = False
    databases.remove(SqlDatabase, skip_if_not_exist=True)
    return is_running_locally
