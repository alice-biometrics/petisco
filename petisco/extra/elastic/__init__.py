from petisco.extra.elastic.is_elastic_available import is_elastic_available

rabbitmq = []
if is_elastic_available():

    from petisco.extra.elastic.elastic_connection import ElasticConnection
    from petisco.extra.elastic.elastic_database import ElasticDatabase

    elastic = ["ElasticConnection", "ElasticDatabase"]
else:
    elastic = []

__all__ = elastic
