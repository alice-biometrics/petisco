from abc import ABCMeta, abstractmethod


class BaseObject:

    __metaclass__ = ABCMeta

    def __init__(self):
        self.guard()

    @abstractmethod
    def guard(self):
        pass
