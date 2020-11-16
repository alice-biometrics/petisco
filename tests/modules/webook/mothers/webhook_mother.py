from petisco import Webhook

DEFAULT_POST_URL = "http://127.0.0.1:5000/webhook"
DEFAULT_API_KEY = "'b0b905d6-228f-44bf-a130-c85d7aecd765"
DEFAULT_SECRET = b"C6CB8A5EFBC81BA9E7DADCB89E3B9"
DEFAULT_EVENT_NAME = "user_created"
DEFAULT_EVENT_VERSION = "1"


class WebhookMother:
    @staticmethod
    def default():
        return Webhook.create(
            post_url=DEFAULT_POST_URL,
            active=True,
            api_key=DEFAULT_API_KEY,
            event_name=DEFAULT_EVENT_NAME,
            event_version=DEFAULT_EVENT_VERSION,
        )

    @staticmethod
    def not_active():
        return Webhook.create(
            post_url=DEFAULT_POST_URL,
            active=False,
            api_key=DEFAULT_API_KEY,
            event_name=DEFAULT_EVENT_NAME,
            event_version=DEFAULT_EVENT_VERSION,
        )

    @staticmethod
    def with_invalid_url():
        return Webhook.create(
            post_url="invalid_url",
            active=True,
            api_key=DEFAULT_API_KEY,
            event_name=DEFAULT_EVENT_NAME,
            event_version=DEFAULT_EVENT_VERSION,
        )
