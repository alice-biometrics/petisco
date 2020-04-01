from meiga import Result, Error, Success

from petisco.security.token_manager.interface_token_manager import ITokenManager
from petisco.domain.aggregate_roots.info_id import InfoId


class NotImplementedTokenManager(ITokenManager):
    def execute(self, headers: dict) -> Result[InfoId, Error]:
        return Success(InfoId.from_headers(headers))
