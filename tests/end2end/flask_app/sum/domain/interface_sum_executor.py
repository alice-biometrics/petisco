from abc import ABCMeta, abstractmethod

from meiga import Result, Error, NotImplementedMethodError

from petisco.application.interface_app_service import IAppService


class ISumExecutor(IAppService):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, value1: int, value2: int) -> Result[int, Error]:
        raise NotImplementedMethodError
