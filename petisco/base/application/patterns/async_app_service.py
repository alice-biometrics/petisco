from abc import abstractmethod
from typing import Any

from meiga import AnyResult, NotImplementedMethodError

from petisco.base.misc.interface import Interface


class AsyncAppService(Interface):
    """
    A base class for creating async app services.
    """

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> AnyResult:
        return NotImplementedMethodError
