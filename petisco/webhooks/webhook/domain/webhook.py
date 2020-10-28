import json
from datetime import datetime
from typing import Dict, Optional

import requests
import validators
from dataclasses import dataclass

from petisco.domain.value_objects.uuid import Uuid
from petisco.webhooks.webhook.domain.invalid_url_error import InvalidUrlError
from petisco.webhooks.webhook.infrastructure.body_digest_signature import (
    BodyDigestSignature,
)

TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


@dataclass
class Webhook:
    post_url: str
    api_key: str
    secret: bytes
    organization: str
    event_name: str
    event_version: Optional[str] = "1"

    def validate(self):
        validation_result = validators.url(self.post_url)
        if not validation_result:
            raise InvalidUrlError()

    def __post_init__(self):
        self.validate()

    def execute(self, payload: Dict):
        headers = self._get_headers()
        auth = self._get_auth()
        requests.post(
            self.post_url, data=json.dumps(payload), headers=headers, auth=auth
        )

    def ping(self):
        headers = self._get_headers()
        auth = self._get_auth()
        payload = {"is_ping": True}
        requests.post(
            self.post_url, data=json.dumps(payload), headers=headers, auth=auth
        )

    def _get_auth(self):
        return BodyDigestSignature(
            secret=self.secret,
            organization=self.organization,
            header=f"X-{self.organization}-Signature",
        )

    def _get_headers(self):
        headers = {
            f"X-{self.organization}-Event": self.event_name,
            f"X-{self.organization}-Event-Version": self.event_version,
            f"X-{self.organization}-Delivery": Uuid.generate().value,
            f"X-{self.organization}-Request-Timestamp": datetime.utcnow().strftime(
                TIME_FORMAT
            ),
            f"User-Agent": f"{self.organization}-Hookshoot/",
            "apikey": self.api_key,
        }
        return headers
