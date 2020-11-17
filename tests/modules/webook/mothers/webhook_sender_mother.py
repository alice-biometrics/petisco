from petisco import WebhookSender

DEFAULT_ORGANIZATION = "Petisco"


class WebhookSenderMother:
    @staticmethod
    def default():
        return WebhookSender(organization=DEFAULT_ORGANIZATION)
