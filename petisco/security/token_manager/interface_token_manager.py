from meiga import Result, Error, NotImplementedMethodError

from abc import ABCMeta, abstractmethod


class ITokenManager:

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, headers: dict) -> Result[str, Error]:
        raise NotImplementedMethodError
