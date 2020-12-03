from abc import ABCMeta, abstractmethod


class BaseObject:

    __metaclass__ = ABCMeta

    def __init__(self, execute_guard: bool = True):
        if execute_guard:
            self.guard()

    @abstractmethod
    def guard(self):
        pass
