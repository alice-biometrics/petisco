import json
from typing import Optional

import validators

from petisco.domain.aggregate_roots.aggregate_root import AggregateRoot
from petisco.webhooks.webhook.domain.invalid_url_error import InvalidUrlError
from petisco.webhooks.webhook.domain.webhook_created import WebhookCreated
from petisco.webhooks.webhook.domain.webhook_id import WebhookId


class Webhook(AggregateRoot):
    @staticmethod
    def create(
        post_url: str, api_key: str, event_name: str, event_version: Optional[str] = "1"
    ):
        webhook_id = WebhookId.generate()

        webhook = Webhook(
            webhook_id=webhook_id,
            post_url=post_url,
            api_key=api_key,
            event_name=event_name,
            event_version=event_version,
        )
        webhook.record(
            WebhookCreated(
                webhook_id=webhook_id,
                subscribed_event_name=event_name,
                subscribed_event_version=event_version,
            )
        )
        return webhook

    @staticmethod
    def from_dict(kdict: dict):
        return Webhook(
            webhook_id=WebhookId(kdict.get("webhook_id")),
            post_url=kdict.get("post_url"),
            api_key=kdict.get("api_key"),
            event_name=kdict.get("event_name"),
            event_version=kdict.get("event_version"),
        )

    def to_dict(self):
        return {
            "webhook_id": self.webhook_id.value,
            "post_url": self.post_url,
            "api_key": self.api_key,
            "event_name": self.api_key,
            "event_version": self.event_version,
        }

    def __init__(
        self,
        webhook_id: WebhookId,
        post_url: str,
        api_key: str,
        event_name: str,
        event_version: Optional[str] = "1",
    ):
        self.webhook_id = webhook_id
        self.post_url = post_url
        self.api_key = api_key
        self.event_name = event_name
        self.event_version = event_version
        self.validate()
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

    def validate(self):
        validation_result = validators.url(self.post_url)

        if not validation_result:
            raise InvalidUrlError()
