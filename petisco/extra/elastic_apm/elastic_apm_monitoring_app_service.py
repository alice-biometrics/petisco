import copy
from abc import abstractmethod

from elasticapm.traces import Transaction, execution_context
from meiga import NotImplementedMethodError, Result

from petisco import AppService


class ElasticApmMonitoringAppService(AppService):
    # This class is built on top of AppService and adds functionalities to instrument the services that are going to be
    # executed in different threads and that we want to keep monitoring.

    @abstractmethod
    def execute(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError

    def _set_transaction(self, transaction: Transaction):
        self.transaction = transaction

    def with_transaction(self, transaction: Transaction):
        service = copy.copy(self)
        service._set_transaction(transaction)
        return service

    def monitoring(self):
        if hasattr(self, "transaction"):
            execution_context.set_transaction(self.transaction)
