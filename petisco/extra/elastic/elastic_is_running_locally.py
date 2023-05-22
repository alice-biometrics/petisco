from petisco.base.domain.persistence.persistence import Persistence
from petisco.extra.elastic.legacy_elastic_database import LegacyElasticDatabase


def elastic_is_running_locally() -> bool:
    try:
        database = LegacyElasticDatabase.local_connection_checker()
        Persistence().add(database)
        Persistence().create()
        is_running_locally = Persistence.is_available(database.name)
    except:  # noqa: E722
        is_running_locally = False
    Persistence().remove("test", skip_if_not_exist=True)
    return is_running_locally
