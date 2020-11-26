import json
from datetime import datetime
from typing import Dict

from meiga import Result, Error, Success

from petisco.webhooks.webhook.domain.webhook import Webhook
from petisco.http.request import Request
from petisco.webhooks.webhook.domain.webhook_result_id import WebhookResultId
from petisco.webhooks.webhook.domain.webhook_result import WebhookResult
from petisco.webhooks.webhook.infrastructure.body_digest_signature import (
    BodyDigestSignature,
)

TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class WebhookSender:
    def __init__(self, organization: str):
        self.organization = organization

    def execute(self, webhook: Webhook, payload: Dict) -> Result[WebhookResult, Error]:
        webhook_delivery_id = WebhookResultId.generate()
        sent_on = datetime.utcnow()
        headers = self._get_headers(webhook, webhook_delivery_id, sent_on)
        auth = self._get_auth(webhook)

        result = Request.post(
            url=webhook.post_url,
            string_info=json.dumps(payload),
            headers=headers,
            auth=auth,
        )
        return Success(
            WebhookResult.create(
                webhook, webhook_delivery_id, sent_on, headers, payload, result
            )
        )

    def ping(self, webhook: Webhook) -> Result[WebhookResult, Error]:
        webhook_delivery_id = WebhookResultId.generate()
        sent_on = datetime.utcnow()
        headers = self._get_headers(webhook, webhook_delivery_id, sent_on)
        auth = self._get_auth(webhook)
        payload = {"is_ping": True}

        result = Request.post(
            url=webhook.post_url,
            string_info=json.dumps(payload),
            headers=headers,
            auth=auth,
        )

        return Success(
            WebhookResult.create(
                webhook, webhook_delivery_id, sent_on, headers, payload, result
            )
        )

    def _get_auth(self, webhook: Webhook):
        return BodyDigestSignature(
            secret=webhook.secret.get_bytes(),
            algorithm=webhook.algorithm.get_algorithm(),
            organization=self.organization,
            header=f"X-{self.organization}-Signature",
        )

    def _get_headers(
        self, webhook: Webhook, webhook_delivery_id: WebhookResultId, sent_on: datetime
    ):
        headers = {
            f"X-{self.organization}-Event": webhook.event_name,
            f"X-{self.organization}-Event-Version": webhook.event_version,
            f"X-{self.organization}-Delivery": webhook_delivery_id.value,
            f"X-{self.organization}-WebhookId": webhook.webhook_id.value,
            f"X-{self.organization}-Request-Timestamp": sent_on.strftime(TIME_FORMAT),
            f"User-Agent": f"{self.organization}-Hookshoot/",
            "apikey": webhook.api_key,
        }
        return headers
