from abc import abstractmethod

from meiga import NotImplementedMethodError, Result

from petisco.base.misc.interface import Interface


class AppService(Interface):
    @abstractmethod
    def execute(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError
