from typing import Any

import pytest
from elasticapm.traces import execution_context
from meiga import Result, isSuccess
from meiga.assertions import assert_success

from petisco.extra.elastic_apm import ElasticApmMonitoringAppService
from tests.modules.extra.decorators import testing_with_elastic


@pytest.mark.integration
class TestElasticApmMonitoringAppService:
    def setup_method(self):
        class MyAppService(ElasticApmMonitoringAppService):
            def execute(self, *args: Any, **kwargs: Any) -> Result:
                return isSuccess

        self.app_service = MyAppService()

    @testing_with_elastic
    def should_execute_the_service_without_transaction(self):
        result = self.app_service.execute()
        assert_success(result)

    @testing_with_elastic
    def should_execute_the_service_with_transaction(self):
        transaction = execution_context.get_transaction()
        app_service = self.app_service.with_transaction(transaction)
        result = app_service.execute()
        assert_success(result)
