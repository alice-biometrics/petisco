from abc import ABCMeta, abstractmethod

from meiga import Result, Error, NotImplementedMethodError

from petisco.security.token_decoder.token import Token


class ITokenDecoder:

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, auth_token) -> Result[Token, Error]:
        return NotImplementedMethodError
