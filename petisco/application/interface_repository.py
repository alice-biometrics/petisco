from abc import ABCMeta, abstractmethod

from meiga import Result, NotImplementedMethodError

from petisco.application.pattern_base import PatternBase


class IRepository(PatternBase):

    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError

    @abstractmethod
    def retrieve(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError

    @abstractmethod
    def retrieve_all(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError

    @abstractmethod
    def remove(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError
