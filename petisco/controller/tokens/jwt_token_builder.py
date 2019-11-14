import jwt


class JwtTokenBuilder:
    @staticmethod
    def build(key, token_type, client_id, issuer="issuer-petisco", user_id=None):
        payload = {
            "iss": issuer,
            "typ": token_type,
            "exp": 1562338273,
            "iat": 1562334673,
            "cli": client_id,
            "sub": user_id,
        }
        token = jwt.encode(payload, key, algorithm="RS256").decode("utf-8")
        return token
