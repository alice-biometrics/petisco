from meiga import Result
from abc import ABCMeta, abstractmethod


class IEventChaos:

    __metaclass__ = ABCMeta

    @abstractmethod
    def info(self):
        return NotImplementedError

    @abstractmethod
    def nack_simulation(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def simulate_failure_on_result(self, result: Result) -> Result:
        raise NotImplementedError

    @abstractmethod
    def delay(self):
        raise NotImplementedError
