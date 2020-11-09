from petisco import WebhookSender

DEFAULT_ORGANIZATION = "Petisco"
DEFAULT_SECRET = b"C6CB8A5EFBC81BA9E7DADCB89E3B9"


class WebhookSenderMother:
    @staticmethod
    def default():
        return WebhookSender(organization=DEFAULT_ORGANIZATION, secret=DEFAULT_SECRET)
