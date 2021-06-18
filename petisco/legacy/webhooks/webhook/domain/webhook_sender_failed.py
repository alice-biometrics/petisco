from dataclasses import dataclass

from petisco.legacy.webhooks.webhook.domain.webhook_result_id import WebhookResultId
from petisco.legacy.event.shared.domain.event import Event
from petisco.legacy.webhooks.webhook.domain.webhook_id import WebhookId


@dataclass
class WebhookSenderFailed(Event):
    webhook_id: WebhookId
    webhook_result_id: WebhookResultId

    def __init__(self, webhook_id: WebhookId, webhook_result_id: WebhookResultId):
        self.webhook_id = webhook_id
        self.webhook_result_id = webhook_result_id
        super().__init__()
