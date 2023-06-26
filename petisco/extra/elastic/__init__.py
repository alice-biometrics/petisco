from petisco.extra.elastic.is_elastic_available import is_elastic_available

elastic = list()
if is_elastic_available():
    from petisco.extra.elastic.async_elastic_database import (
        AsyncElasticDatabase,
        AsyncElasticSessionScope,
    )
    from petisco.extra.elastic.elastic_connection import ElasticConnection
    from petisco.extra.elastic.elastic_database import (
        ElasticDatabase,
        ElasticSessionScope,
    )
    from petisco.extra.elastic.legacy_elastic_database import LegacyElasticDatabase

    elastic = [
        "ElasticConnection",
        "LegacyElasticDatabase",
        "ElasticDatabase",
        "AsyncElasticDatabase",
        "ElasticSessionScope",
        "AsyncElasticSessionScope",
    ]
else:
    elastic = []

__all__ = elastic
