import json
from datetime import datetime
from typing import Dict

from meiga import Result, Error

from petisco.webhooks.webhook.domain.webhook import Webhook
from petisco.domain.value_objects.uuid import Uuid
from petisco.http.request import Request
from petisco.http.response import Response
from petisco.webhooks.webhook.infrastructure.body_digest_signature import (
    BodyDigestSignature,
)

TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class WebhookSender:
    def __init__(self, organization: str, secret: bytes):
        self.organization = organization
        self.secret = secret

    def execute(self, webhook: Webhook, payload: Dict) -> Result[Response, Error]:
        headers = self._get_headers(webhook)
        auth = self._get_auth()

        return Request.post(
            url=webhook.post_url,
            string_info=json.dumps(payload),
            headers=headers,
            auth=auth,
        )

    def ping(self, webhook: Webhook) -> Result[Response, Error]:
        headers = self._get_headers(webhook)
        auth = self._get_auth()
        payload = {"is_ping": True}

        return Request.post(
            url=webhook.post_url,
            string_info=json.dumps(payload),
            headers=headers,
            auth=auth,
        )

    def _get_auth(self):
        return BodyDigestSignature(
            secret=self.secret,
            organization=self.organization,
            header=f"X-{self.organization}-Signature",
        )

    def _get_headers(self, webhook: Webhook):
        headers = {
            f"X-{self.organization}-Event": webhook.event_name,
            f"X-{self.organization}-Event-Version": webhook.event_version,
            f"X-{self.organization}-Delivery": Uuid.generate().value,
            f"X-{self.organization}-WebhookId": webhook.webhook_id.value,
            f"X-{self.organization}-Request-Timestamp": datetime.utcnow().strftime(
                TIME_FORMAT
            ),
            f"User-Agent": f"{self.organization}-Hookshoot/",
            "apikey": webhook.api_key,
        }
        return headers
