from typing import Optional

from pydantic.main import BaseModel

from petisco.base.domain.ids.client_id import ClientId
from petisco.base.domain.ids.correlation_id import CorrelationId
from petisco.base.domain.ids.user_id import UserId


class InfoId(BaseModel):
    client_id: Optional[ClientId] = None
    user_id: Optional[UserId] = None
    correlation_id: Optional[CorrelationId] = None
    ip: Optional[str] = None  # TODO Review IPv4Address

    def __init__(
        self,
        client_id: Optional[ClientId] = None,
        user_id: Optional[UserId] = None,
        correlation_id: Optional[CorrelationId] = None,
        ip: Optional[str] = None,
        **data
    ) -> None:
        super().__init__(
            client_id=client_id,
            user_id=user_id,
            correlation_id=correlation_id,
            ip=ip,
            **data
        )

    @staticmethod
    def from_headers(headers: dict):
        if headers:
            info_id = InfoId(
                client_id=headers.get("X-Onboarding-Clientid"),
                user_id=headers.get("X-Onboarding-Userid"),
                correlation_id=headers.get("X-Correlation-Id"),
                ip=headers.get("X-Forwarded-For"),
            )
        else:
            info_id = InfoId()
        return info_id

    def get_http_headers(self):
        headers = {}

        if self.client_id:
            headers["X-Onboarding-Clientid"] = self.client_id.value
        if self.user_id:
            headers["X-Onboarding-Userid"] = self.user_id.value
        if self.correlation_id:
            headers["X-Correlation-Id"] = self.correlation_id.value
        if self.ip:
            headers["X-Forwarded-For"] = str(self.ip)

        return headers if len(headers) > 0 else None
