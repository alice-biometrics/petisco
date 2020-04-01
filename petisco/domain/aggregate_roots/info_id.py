from typing import Any, Dict

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from meiga import Result, Error, Success
from meiga.decorators import meiga
from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.user_id import UserId
from petisco.domain.value_objects.correlation_id import CorrelationId
from petisco.domain.aggregate_roots.aggregate_root import AggregateRoot
from petisco.security.token_decoder.token import Token


@dataclass_json
@dataclass
class InfoId(AggregateRoot):
    client_id: ClientId = None
    user_id: UserId = None
    correlation_id: CorrelationId = None

    def __init__(
        self,
        client_id: ClientId = None,
        user_id: UserId = None,
        correlation_id: CorrelationId = None,
    ):
        self.client_id = client_id
        self.user_id = user_id
        self.correlation_id = (
            correlation_id if correlation_id else CorrelationId.generate()
        )
        super().__init__()

    def __repr__(self):
        return f"[InfoId: [client_id: {self.client_id} | user_id: {self.user_id} | correlation_id: {self.correlation_id}]]"

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.client_id == other.client_id
            and self.user_id == other.user_id
            and self.correlation_id == other.correlation_id
        )

    def update_from_headers(self, headers: Dict[str, str]):
        if headers:
            client_id = headers.get("X-Onboarding-Clientid")
            user_id = headers.get("X-Onboarding-Userid")
            correlation_id = headers.get("X-Correlation-Id")

            self.client_id = client_id if client_id else self.client_id
            self.user_id = user_id if user_id else self.user_id
            self.correlation_id = (
                correlation_id if correlation_id else self.correlation_id
            )
        return self

    @staticmethod
    def from_headers(headers: Dict[str, str]):
        if headers:
            info_id = InfoId.from_strings(
                headers.get("X-Onboarding-Clientid"),
                headers.get("X-Onboarding-Userid"),
                headers.get("X-Correlation-Id"),
            )
        else:
            info_id = InfoId()
        return info_id

    @staticmethod
    def from_token(token: Token):
        if token:
            info_id = InfoId.from_strings(token.client_id, token.user_id)
        else:
            info_id = InfoId()
        return info_id

    @staticmethod
    def from_strings(
        client_id: str = None, user_id: str = None, correlation_id: str = None
    ):
        return InfoId(
            ClientId(client_id) if client_id else None,
            UserId(user_id) if user_id else None,
            CorrelationId(correlation_id) if correlation_id else None,
        )

    @meiga
    def to_result(self) -> Result[Any, Error]:
        if self.client_id:
            self.client_id.guard()

        if self.user_id:
            self.user_id.guard()

        return Success(self)

    def get_http_headers(self):
        headers = {}

        if self.client_id:
            headers["X-Onboarding-Clientid"] = self.client_id
        if self.user_id:
            headers["X-Onboarding-Userid"] = self.user_id
        if self.correlation_id:
            headers["X-Correlation-Id"] = self.correlation_id

        return headers if len(headers) > 0 else None
