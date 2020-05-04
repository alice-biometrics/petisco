from abc import ABCMeta, abstractmethod
from typing import Dict

from meiga import Result, NotImplementedMethodError


class IRepository:

    __metaclass__ = ABCMeta

    @abstractmethod
    def info(self) -> Dict:
        return {"Repository": "Not Implemented"}

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
