from abc import ABCMeta, abstractmethod
from typing import Dict

from meiga import Result, NotImplementedMethodError


class IService:

    __metaclass__ = ABCMeta

    @abstractmethod
    def info(self) -> Dict:
        return {"Service": "Not Implemented"}

    @abstractmethod
    def execute(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError
