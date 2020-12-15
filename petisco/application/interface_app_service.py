from abc import ABCMeta, abstractmethod

from meiga import Result, NotImplementedMethodError

from petisco.application.pattern_base import PatternBase


class IAppService(PatternBase):

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError


# Deprecated
class IService(PatternBase):

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError
