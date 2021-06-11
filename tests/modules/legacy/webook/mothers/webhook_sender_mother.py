from petisco.legacy import WebhookSender

DEFAULT_ORGANIZATION = "Petisco"


class WebhookSenderMother:
    @staticmethod
    def default():
        return WebhookSender(organization=DEFAULT_ORGANIZATION)
