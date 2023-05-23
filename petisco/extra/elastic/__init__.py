from petisco.extra.elastic.is_elastic_available import is_elastic_available

elastic = list()
if is_elastic_available():
    from petisco.extra.elastic.elastic_connection import ElasticConnection
    from petisco.extra.elastic.elastic_database import ElasticDatabase
    from petisco.extra.elastic.legacy_elastic_database import LegacyElasticDatabase

    elastic = ["ElasticConnection", "LegacyElasticDatabase", "ElasticDatabase"]
else:
    elastic = []

__all__ = elastic
