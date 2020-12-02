from abc import ABCMeta, abstractmethod

from meiga import Result, Error, NotImplementedMethodError

from petisco.application.interface_application_service import IApplicationService


class ISumExecutor(IApplicationService):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, value1: int, value2: int) -> Result[int, Error]:
        raise NotImplementedMethodError
