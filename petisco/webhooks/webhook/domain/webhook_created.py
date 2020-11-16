from dataclasses import dataclass

from petisco.event.shared.domain.event import Event
from petisco.webhooks.webhook.domain.webhook_id import WebhookId


@dataclass
class WebhookCreated(Event):
    webhook_id: WebhookId
    active: bool
    subscribed_event_name: str
    subscribed_event_version: str

    def __init__(
        self,
        webhook_id: WebhookId,
        active: bool,
        subscribed_event_name: str,
        subscribed_event_version: str,
    ):
        self.webhook_id = webhook_id
        self.active = active
        self.subscribed_event_name = subscribed_event_name
        self.subscribed_event_version = subscribed_event_version
        super().__init__()
