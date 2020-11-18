import json
from datetime import datetime
from dateutil import parser
from meiga import Result

from petisco.domain.aggregate_roots.aggregate_root import AggregateRoot
from petisco.webhooks.webhook.domain.webhook_delivery_id import WebhookDeliveryId
from petisco.webhooks.webhook.domain.webhook_request_result import WebhookRequestResult
from petisco.webhooks.webhook.domain.webhook_response_result import (
    WebhookResponseResult,
)


class WebhookResult(AggregateRoot):
    @staticmethod
    def create(
        webhook_delivery_id: WebhookDeliveryId,
        sent_on: datetime,
        request_headers: dict,
        request_body: dict,
        result: Result,
    ):
        response = WebhookResponseResult.from_result(result)
        request = WebhookRequestResult(request_headers, request_body)
        return WebhookResult(
            webhook_delivery_id, sent_on, response, request, result.is_success
        )

    @staticmethod
    def from_dict(kdict: dict):
        sent_on = kdict.get("sent_on")
        if isinstance(sent_on, str):
            sent_on = parser.parse(kdict.get("sent_on"))
        return WebhookResult(
            webhook_delivery_id=WebhookDeliveryId(kdict.get("webhook_delivery_id")),
            sent_on=sent_on,
            response=WebhookResponseResult.from_dict(kdict.get("response"))
            if kdict.get("response")
            else None,
            request=WebhookRequestResult.from_dict(kdict.get("request"))
            if kdict.get("request")
            else None,
            is_success=kdict.get("is_success"),
        )

    def to_dict(self):
        return {
            "webhook_delivery_id": self.webhook_delivery_id.value,
            "sent_on": str(self.sent_on),
            "response": self.response.to_dict() if self.response else None,
            "request": self.request.to_dict() if self.request else None,
            "is_success": self.is_success,
        }

    def __init__(
        self,
        webhook_delivery_id: WebhookDeliveryId,
        sent_on: datetime,
        response: WebhookResponseResult,
        request: WebhookRequestResult,
        is_success: bool,
    ):
        self.webhook_delivery_id = webhook_delivery_id
        self.sent_on = sent_on
        self.response = response
        self.request = request
        self.is_success = is_success
        super().__init__()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if issubclass(other.__class__, self.__class__) or issubclass(
            self.__class__, other.__class__
        ):
            return self.to_dict() == other.to_dict()
        else:
            return False
