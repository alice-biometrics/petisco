import jwt

from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.user_id import UserId


class JwtTokenBuilder:
    @staticmethod
    def build(
        key: str,
        token_type,
        client_id: ClientId,
        issuer="issuer-petisco",
        user_id: UserId = None,
    ):
        payload = {
            "iss": issuer,
            "typ": token_type,
            "exp": 1562338273,
            "iat": 1562334673,
            "cli": client_id.value,
            "sub": user_id.value if user_id else None,
        }
        token = jwt.encode(payload, key, algorithm="RS256").decode("utf-8")
        return token
