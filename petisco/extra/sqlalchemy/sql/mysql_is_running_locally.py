from petisco.base.domain.persistence.persistence import Persistence


def mysql_is_running_locally() -> bool:
    try:
        from petisco.extra.sqlalchemy.sql.mysql.legacy_mysql_database import (
            LegacyMySqlDatabase,
        )

        database = LegacyMySqlDatabase.local_connection_checker()
        Persistence().add(database)
        Persistence().create()
        is_running_locally = True
    except:  # noqa: E722
        is_running_locally = False
    Persistence().remove("test", skip_if_not_exist=True)
    return is_running_locally
