from typing import Any

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from meiga import Result, Error, Success
from meiga.decorators import meiga
from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.user_id import UserId
from petisco.domain.value_objects.correlation_id import CorrelationId
from petisco.domain.aggregate_roots.aggregate_root import AggregateRoot


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
        self.correlation_id = correlation_id
        super().__init__()

    def __repr__(self):
        return f"[InfoId: [client_id: {self.client_id} | user_id: {self.user_id} | correlation_id: {self.correlation_id}]]"

    @staticmethod
    def from_strings(
        client_id: str = None, user_id: str = None, correlation_id: str = None
    ):
        return InfoId(
            ClientId(client_id), UserId(user_id), CorrelationId(correlation_id)
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
            headers["X-Onboarding-ClientId"] = self.client_id
        if self.user_id:
            headers["X-Onboarding-UserId"] = self.user_id
        if self.correlation_id:
            headers["X-Correlation-Id"] = self.correlation_id

        return headers if len(headers) > 0 else None
