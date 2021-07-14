from abc import abstractmethod

from meiga import NotImplementedMethodError, Result

from petisco.base.application.patterns.base_pattern import BasePattern


class Repository(BasePattern):
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
