from abc import abstractmethod

from petisco.base.misc.interface import Interface


class Builder(Interface):
    @abstractmethod
    def build(self):
        raise NotImplementedError()
