from petisco.extra.elastic.is_elastic_available import is_elastic_available
from petisco.extra.elastic_apm.is_elastic_apm_available import is_elastic_apm_available

elastic_apm = []
if is_elastic_available() or is_elastic_apm_available():
    from petisco.extra.elastic_apm.elastic_apm_monitoring_app_service import (
        ElasticApmMonitoringAppService,
    )

    elastic_apm = ["ElasticApmMonitoringAppService"]
else:
    elastic_apm = []

__all__ = elastic_apm
