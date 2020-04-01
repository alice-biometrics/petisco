from meiga import Result, Error, Success, Failure, isSuccess
from meiga.decorators import meiga

from petisco.security.token_decoder.invalid_token_error import InvalidTokenError
from petisco.security.token_manager.interface_token_manager import ITokenManager
from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.security.token_decoder.interface_token_decoder import ITokenDecoder
from petisco.security.token_decoder.token_decoder import TokenDecoder


class TokenManager(ITokenManager):
    def __init__(
        self,
        token_type: str,
        require_user: bool = False,
        token_decoder: ITokenDecoder = TokenDecoder(),
    ):
        self.token_type = token_type
        self.require_user = require_user
        self.token_decoder = token_decoder

    @meiga
    def execute(self, headers: dict) -> Result[InfoId, Error]:
        auth_token = headers.get("Authorization")

        if not auth_token:
            return Failure(
                InvalidTokenError(
                    message=f"This entry point expects a valid {self.token_type} Token"
                )
            )

        token = self.token_decoder.execute(auth_token).unwrap_or_return()

        self.ensure_required_token(token).unwrap_or_return()

        info_id = InfoId.from_token(token).update_from_headers(headers)

        return Success(info_id)

    def ensure_required_token(self, token) -> Result[bool, Error]:
        if (
            token.token_type != self.token_type
            or (self.require_user and not token.user_id)
            or (not self.require_user and token.user_id)
        ):
            return Failure(
                InvalidTokenError(
                    message=f"This entry point expects a valid {self.token_type} Token"
                )
            )
        return isSuccess
