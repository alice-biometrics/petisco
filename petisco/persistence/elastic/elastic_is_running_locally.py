from petisco.persistence.elastic.elastic_database import ElasticDatabase
from petisco.persistence.persistence import Persistence


def elastic_is_running_locally() -> bool:
    try:
        database = ElasticDatabase.local_connection_checker()
        Persistence().add(database)
        Persistence().create()
        is_running_locally = Persistence.get_session(database.name).ping()
        Persistence().remove("test")
    except:  # noqa: E722
        is_running_locally = False
    return is_running_locally
