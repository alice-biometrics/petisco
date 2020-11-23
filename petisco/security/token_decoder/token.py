from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.user_id import UserId


class Token:
    def __init__(self, client_id: ClientId, user_id: UserId, token_type: str):
        self.client_id = client_id
        self.user_id = user_id
        self.token_type = token_type

        if not self.user_id or self.user_id == "null":
            self.user_id = None

    def __repr__(self):
        return f"[Token: [{self.client_id} | user_id: {self.user_id} | token_type: {self.token_type}]]"

    @staticmethod
    def from_token_payload(token_payload: dict):
        return Token(
            client_id=ClientId(token_payload.get("cli")),
            user_id=UserId(token_payload.get("sub"))
            if token_payload.get("sub")
            else None,
            token_type=token_payload.get("typ"),
        )
