from petisco.base.domain.persistence.databases import databases
from petisco.extra.elastic.elastic_database import ElasticDatabase


def elastic_is_running_locally() -> bool:
    try:
        alias = "local"
        database = ElasticDatabase.local_connection_checker(alias=alias)
        databases.add(database)
        databases.initialize()
        is_running_locally = databases.get(ElasticDatabase, alias=alias).is_available()
    except:  # noqa: E722
        is_running_locally = False
    databases.remove(ElasticDatabase, alias=alias, skip_if_not_exist=True)
    return is_running_locally
