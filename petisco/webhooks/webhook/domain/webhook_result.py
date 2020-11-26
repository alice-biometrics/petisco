import json
from datetime import datetime
from meiga import Result

from petisco.domain.date_parser import DateParser
from petisco.webhooks.webhook.domain.webhook_id import WebhookId
from petisco.webhooks.webhook.domain.webhook import Webhook
from petisco.domain.aggregate_roots.aggregate_root import AggregateRoot
from petisco.webhooks.webhook.domain.webhook_sender_failed import WebhookSenderFailed
from petisco.webhooks.webhook.domain.webhook_result_id import WebhookResultId
from petisco.webhooks.webhook.domain.webhook_request_result import WebhookRequestResult
from petisco.webhooks.webhook.domain.webhook_response_result import (
    WebhookResponseResult,
)


class WebhookResult(AggregateRoot):
    @staticmethod
    def create(
        webhook: Webhook,
        webhook_result_id: WebhookResultId,
        sent_on: datetime,
        request_headers: dict,
        request_body: dict,
        result: Result,
    ):
        response = WebhookResponseResult.from_result(result)
        request = WebhookRequestResult(request_headers, request_body)
        webhook_result = WebhookResult(
            webhook_result_id,
            webhook.webhook_id,
            sent_on,
            response,
            request,
            result.is_success,
        )

        if not webhook_result.is_success:
            webhook_result.record(
                WebhookSenderFailed(
                    webhook_id=webhook.webhook_id, webhook_result_id=webhook_result_id
                )
            )

        return webhook_result

    @staticmethod
    def from_dict(kdict: dict):
        return WebhookResult(
            webhook_result_id=WebhookResultId(kdict.get("webhook_result_id")),
            webhook_id=WebhookId(kdict.get("webhook_id")),
            sent_on=DateParser.datetime_from_str(kdict.get("sent_on")),
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
            "webhook_result_id": self.webhook_result_id.value,
            "webhook_id": self.webhook_id.value,
            "sent_on": DateParser.str_from_datetime(self.sent_on),
            "response": self.response.to_dict() if self.response else None,
            "request": self.request.to_dict() if self.request else None,
            "is_success": self.is_success,
        }

    def __init__(
        self,
        webhook_result_id: WebhookResultId,
        webhook_id: WebhookId,
        sent_on: datetime,
        response: WebhookResponseResult,
        request: WebhookRequestResult,
        is_success: bool,
    ):
        self.webhook_result_id = webhook_result_id
        self.webhook_id = webhook_id
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
