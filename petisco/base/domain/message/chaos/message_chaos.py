from abc import abstractmethod
from typing import Any

from petisco.base.misc.interface import Interface


class MessageChaos(Interface):
    @abstractmethod
    def nack_simulation(self, *args: Any, **kwargs: Any) -> bool:
        raise NotImplementedError

    @abstractmethod
    def failure_simulation(self, *args: Any, **kwargs: Any) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delay(self) -> None:
        raise NotImplementedError
