from abc import ABCMeta, abstractmethod
from typing import Dict

from meiga import Result, NotImplementedMethodError


class IService:

    __metaclass__ = ABCMeta

    @classmethod
    def info(cls) -> Dict:
        return {"name": cls.__name__}

    @abstractmethod
    def execute(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError
