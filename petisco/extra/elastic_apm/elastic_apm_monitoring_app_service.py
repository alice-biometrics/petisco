import copy
from abc import abstractmethod
from typing import Any, Dict

from elasticapm.traces import Transaction, execution_context
from meiga import AnyResult, NotImplementedMethodError

from petisco.base.application.patterns.app_service import AppService


class ElasticApmMonitoringAppService(AppService):
    # This class is built on top of AppService and adds functionalities to instrument the services that are going to be
    # executed in different threads and that we want to keep monitoring.

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Dict[str, Any]) -> AnyResult:
        return NotImplementedMethodError

    def _set_transaction(self, transaction: Transaction) -> None:
        self.transaction = transaction

    def with_transaction(self, transaction: Transaction) -> "ElasticApmMonitoringAppService":
        service = copy.copy(self)
        service._set_transaction(transaction)
        return service

    def monitoring(self) -> None:
        if hasattr(self, "transaction"):
            execution_context.set_transaction(self.transaction)
