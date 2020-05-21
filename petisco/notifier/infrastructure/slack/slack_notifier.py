from typing import Dict

from petisco.notifier.domain.interface_notifier import INotifier
from slack import WebClient
from slack.errors import SlackApiError

from petisco.notifier.domain.notifier_message import NotifierMessage


class SlackNotifier(INotifier):
    def __init__(self, token: str):
        self.token = token

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def publish(self, notifier_message: NotifierMessage):

        client = WebClient(token=self.token)

        try:
            response = client.chat_postMessage(channel="#random", text="Hello world!")
            assert response["message"]["text"] == "Hello world!"
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")
