from abc import abstractmethod
from typing import Any

from meiga import AnyResult, NotImplementedMethodError

from petisco.base.misc.interface import Interface


class AppService(Interface):
    """
    A base class for creating app services.
    """

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> AnyResult:
        return NotImplementedMethodError
