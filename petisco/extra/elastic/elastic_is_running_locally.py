from petisco.base.domain.persistence.databases import databases
from petisco.extra.elastic.elastic_database import ElasticDatabase


def elastic_is_running_locally() -> bool:
    try:
        database = ElasticDatabase.local_connection_checker()
        databases.add(database)
        databases.initialize()
        is_running_locally = databases.get(ElasticDatabase).is_available()
    except:  # noqa: E722
        is_running_locally = False
    databases.remove(ElasticDatabase, skip_if_not_exist=True)
    return is_running_locally
