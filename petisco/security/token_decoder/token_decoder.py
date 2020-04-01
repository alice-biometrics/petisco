import base64
import json

from meiga import Result, Error, Failure, Success
from meiga.decorators import meiga

from petisco.security.token_decoder.interface_token_decoder import ITokenDecoder
from petisco.security.token_decoder.invalid_token_error import InvalidTokenError
from petisco.security.token_decoder.token import Token


class TokenDecoder(ITokenDecoder):
    @meiga
    def execute(self, auth_token) -> Result[Token, Error]:
        token_payload = self.decode_token_payload(auth_token).unwrap_or_return()
        return Success(Token.from_token_payload(token_payload))

    def decode_token_payload(self, token):
        try:
            token_payload = token.split(".")[1]
            token_payload += "=" * ((4 - len(token_payload) % 4) % 4)
            token_payload = json.loads(base64.b64decode(token_payload).decode("utf-8"))
        except (IndexError, AttributeError):
            return Failure(InvalidTokenError())

        return Success(token_payload)
