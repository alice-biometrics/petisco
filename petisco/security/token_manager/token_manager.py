from typing import List

from meiga import Result, Error, Success, Failure, isSuccess, BoolResult
from meiga.decorators import meiga

from petisco.security.token_decoder.invalid_token_error import InvalidTokenError
from petisco.security.token_decoder.token import Token
from petisco.security.token_manager.accepted_token import AcceptedToken
from petisco.security.token_manager.interface_token_manager import ITokenManager
from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.security.token_decoder.interface_token_decoder import ITokenDecoder
from petisco.security.token_decoder.token_decoder import TokenDecoder


class TokenManager(ITokenManager):
    def __init__(
        self,
        accepted_tokens=List[AcceptedToken],
        token_decoder: ITokenDecoder = TokenDecoder(),
    ):
        self.accepted_tokens = accepted_tokens
        self.token_decoder = token_decoder

    @meiga
    def execute(self, headers: dict) -> Result[InfoId, Error]:
        auth_token = headers.get("Authorization")

        if not auth_token:
            return Failure(
                InvalidTokenError(
                    message=f"This entry point expects a valid {self.accepted_tokens.token_type} Token"
                )
            )

        token = self.token_decoder.execute(auth_token).unwrap_or_return()

        self.ensure_required_token(token).unwrap_or_return()

        info_id = InfoId.from_token(token).update_from_headers(headers)

        return Success(info_id)

    @meiga
    def ensure_required_token(self, token: Token) -> BoolResult:
        result = isSuccess
        for accepted_token in self.accepted_tokens:
            result = accepted_token.check(token)
            if result.is_success:
                break
        result.unwrap_or_return()
        return isSuccess
