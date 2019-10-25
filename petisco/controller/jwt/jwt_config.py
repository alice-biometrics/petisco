class JwtConfig:
    def __init__(self, token_type: str, require_user: bool = False):
        self.token_type = token_type
        self.require_user = require_user
