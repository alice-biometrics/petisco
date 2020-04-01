class Token:
    def __init__(self, client_id: str, user_id: str, token_type: str):
        self.client_id = client_id
        self.user_id = user_id
        self.token_type = token_type

        if not self.user_id or self.user_id == "null":
            self.user_id = None

    def __repr__(self):
        return f"[Token: [client_id: {self.client_id} | user_id: {self.user_id} | token_type: {self.token_type}]]"

    @staticmethod
    def from_token_payload(token_payload: dict):
        return Token(
            client_id=token_payload.get("cli"),
            user_id=token_payload.get("sub"),
            token_type=token_payload.get("typ"),
        )
