from abc import ABCMeta, abstractmethod

from meiga import Result


class DeployTestBase(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, verbose: bool = False) -> Result:
        raise NotImplementedError
