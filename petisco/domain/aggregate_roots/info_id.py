from typing import Dict, Optional

from dataclasses import dataclass
from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.user_id import UserId
from petisco.domain.value_objects.correlation_id import CorrelationId
from petisco.domain.aggregate_roots.aggregate_root import AggregateRoot
from petisco.security.token_decoder.token import Token


@dataclass
class InfoId(AggregateRoot):
    client_id: Optional[ClientId] = None
    user_id: Optional[UserId] = None
    correlation_id: Optional[CorrelationId] = None
    ip: Optional[str] = None

    def __init__(
        self,
        client_id: ClientId = None,
        user_id: UserId = None,
        correlation_id: CorrelationId = None,
        ip: str = None,
    ):
        self.client_id = client_id
        self.user_id = user_id
        self.correlation_id = (
            correlation_id if correlation_id else CorrelationId.generate()
        )
        self.ip = ip
        super().__init__()

    def __repr__(self):
        return f"[InfoId: [client_id: {self.client_id} | user_id: {self.user_id} | correlation_id: {self.correlation_id} | ip: {self.ip}]]"

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.client_id == other.client_id
            and self.user_id == other.user_id
            and self.correlation_id == other.correlation_id
            and self.ip == other.ip
        )

    @staticmethod
    def from_dict(kdict: dict):
        client_id = ClientId(kdict.get("client_id")) if kdict.get("client_id") else None
        user_id = ClientId(kdict.get("user_id")) if kdict.get("user_id") else None
        correlation_id = (
            ClientId(kdict.get("correlation_id"))
            if kdict.get("correlation_id")
            else None
        )
        ip = kdict.get("ip")

        return InfoId(
            client_id=client_id, user_id=user_id, correlation_id=correlation_id, ip=ip
        )

    def to_dict(self):
        return {
            "client_id": self.client_id.value if self.client_id else None,
            "user_id": self.user_id.value if self.user_id else None,
            "correlation_id": self.correlation_id.value
            if self.correlation_id
            else None,
            "ip": self.ip,
        }

    def update_from_headers(self, headers: Dict[str, str]):
        if headers:
            client_id = headers.get("X-Onboarding-Clientid")
            user_id = headers.get("X-Onboarding-Userid")
            correlation_id = headers.get("X-Correlation-Id")
            ip = headers.get("X-Forwarded-For")

            self.client_id = ClientId(client_id) if client_id else self.client_id
            self.user_id = UserId(user_id) if user_id else self.user_id
            self.correlation_id = (
                CorrelationId(correlation_id) if correlation_id else self.correlation_id
            )
            self.ip = ip if ip else self.ip
        return self

    @staticmethod
    def from_headers(headers: Dict[str, str]):
        if headers:
            info_id = InfoId.from_strings(
                headers.get("X-Onboarding-Clientid"),
                headers.get("X-Onboarding-Userid"),
                headers.get("X-Correlation-Id"),
                headers.get("X-Forwarded-For"),
            )
        else:
            info_id = InfoId()
        return info_id

    @staticmethod
    def from_token(token: Token):
        if token:
            info_id = InfoId.from_strings(
                token.client_id.value, token.user_id.value if token.user_id else None
            )
        else:
            info_id = InfoId()
        return info_id

    @staticmethod
    def from_strings(
        client_id: str = None,
        user_id: str = None,
        correlation_id: str = None,
        ip: str = None,
    ):
        return InfoId(
            ClientId(client_id) if client_id else None,
            UserId(user_id) if user_id else None,
            CorrelationId(correlation_id) if correlation_id else None,
            ip,
        )

    def get_http_headers(self):
        headers = {}

        if self.client_id:
            headers["X-Onboarding-Clientid"] = self.client_id.value
        if self.user_id:
            headers["X-Onboarding-Userid"] = self.user_id.value
        if self.correlation_id:
            headers["X-Correlation-Id"] = self.correlation_id.value

        return headers if len(headers) > 0 else None
