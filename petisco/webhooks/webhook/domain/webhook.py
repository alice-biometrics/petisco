from typing import Dict

import requests
import validators
from dataclasses import dataclass

from petisco.domain.value_objects.uuid import Uuid
from petisco.webhooks.webhook.domain.invalid_url_error import InvalidUrlError
from petisco.webhooks.webhook.infrastructure.body_digest_signature import (
    BodyDigestSignature,
)


@dataclass
class Webhook:
    post_url: str
    api_key: str
    secret: bytes
    event_triggered: str
    organization: str

    def validate(self):
        validation_result = validators.url(self.post_url)
        if not validation_result:
            raise InvalidUrlError()

    def __post_init__(self):
        self.validate()

    def execute(self, payload: Dict):
        headers = self._get_headers()
        auth = self._get_auth()
        requests.post(self.post_url, json=payload, headers=headers, auth=auth)

    def ping(self):
        headers = self._get_headers()
        auth = self._get_auth()
        payload = {"is_ping": True}
        requests.post(self.post_url, json=payload, headers=headers, auth=auth)

    def _get_auth(self):
        return BodyDigestSignature(
            secret=self.secret, header=f"X-{self.organization}-Signature"
        )

    def _get_headers(self):
        headers = {
            f"X-{self.organization}-Event": self.event_triggered,
            f"X-{self.organization}-Delivery": Uuid.generate().value,
            # f"X-{self.organization}-Signature": self.secret,
            f"User-Agent": f"{self.organization}-Hookshoot/",
            "apikey": self.api_key,
        }
        return headers
