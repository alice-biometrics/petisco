from abc import ABCMeta, abstractmethod
from typing import Any

from meiga import Result, Error, NotImplementedMethodError


class BaseObject:

    __metaclass__ = ABCMeta

    @abstractmethod
    def to_result(self) -> Result[Any, Error]:
        return NotImplementedMethodError

    def guard(self):
        return self.to_result().unwrap_or_return()
