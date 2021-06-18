from petisco.legacy.persistence.elastic.elastic_database import ElasticDatabase
from petisco.legacy.persistence.persistence import Persistence


def elastic_is_running_locally() -> bool:
    try:
        database = ElasticDatabase.local_connection_checker()
        Persistence().add(database)
        Persistence().create()
        is_running_locally = Persistence.is_available(database.name)
    except:  # noqa: E722
        is_running_locally = False
    Persistence().remove("test", skip_if_not_exist=True)
    return is_running_locally
