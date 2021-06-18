from abc import ABCMeta, abstractmethod
from meiga import Result


class UseCase:

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, *args, **kwargs) -> Result:
        raise Result(failure=NotImplementedError())
