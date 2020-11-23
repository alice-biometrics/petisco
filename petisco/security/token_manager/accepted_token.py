from meiga import Failure, isSuccess, BoolResult

from petisco.security.token_decoder.invalid_token_error import InvalidTokenError
from petisco.security.token_decoder.token import Token


class AcceptedToken:
    def __init__(self, token_type: str, require_user: bool = False):
        self.token_type = token_type
        self.require_user = require_user

    @staticmethod
    def user():
        return AcceptedToken(token_type="USER", require_user=True)

    @staticmethod
    def backend():
        return AcceptedToken(token_type="BACKEND")

    @staticmethod
    def backend_with_user():
        return AcceptedToken(token_type="BACKEND", require_user=True)

    def check(self, token: Token) -> BoolResult:
        if (
            token.token_type != self.token_type
            or (self.require_user and not token.user_id)
            or (not self.require_user and token.user_id)
        ):
            return Failure(
                InvalidTokenError(
                    message=f"This entry point expects a valid {self.token_type} Token with require_user={self.require_user}"
                )
            )
        return isSuccess
