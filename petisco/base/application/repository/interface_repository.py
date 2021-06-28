from abc import abstractmethod

from meiga import Result, NotImplementedMethodError

from petisco.base.application.repository.pattern_base import PatternBase


class Repository(PatternBase):
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
