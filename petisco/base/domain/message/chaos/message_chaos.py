from abc import abstractmethod

from petisco.base.misc.interface import Interface


class MessageChaos(Interface):
    @abstractmethod
    def nack_simulation(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def failure_simulation(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delay(self):
        raise NotImplementedError
