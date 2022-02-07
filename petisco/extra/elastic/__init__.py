from petisco.extra.elastic.is_elastic_available import is_elastic_available

rabbitmq = list()
if is_elastic_available():

    from petisco.extra.elastic.elastic_apm_monitoring_app_service import (
        ElasticApmMonitoringAppService,
    )
    from petisco.extra.elastic.elastic_connection import ElasticConnection
    from petisco.extra.elastic.elastic_database import ElasticDatabase

    elastic = ["ElasticConnection", "ElasticDatabase", "ElasticApmMonitoringAppService"]
else:
    elastic = []

__all__ = elastic
