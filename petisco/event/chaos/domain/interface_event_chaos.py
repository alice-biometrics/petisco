from typing import Dict

from abc import ABCMeta, abstractmethod


class IEventChaos:

    __metaclass__ = ABCMeta

    @abstractmethod
    def info(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def nack_simulation(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def failure_simulation(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delay(self):
        raise NotImplementedError
