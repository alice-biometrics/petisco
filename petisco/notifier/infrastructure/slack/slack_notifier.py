from typing import Dict

from slack import WebClient
from slack.errors import SlackApiError

from petisco.notifier.domain.interface_notifier import INotifier
from petisco.notifier.domain.notifier_message import NotifierMessage
from petisco.notifier.infrastructure.slack.interface_slack_notifier_message_converter import (
    ISlackNotifierMessageConverter,
)
from petisco.notifier.infrastructure.slack.slack_notifier_message_converter import (
    SlackNotifierMessageConverter,
)


class SlackNotifier(INotifier):
    def __init__(
        self,
        token: str,
        channel: str,
        converter: ISlackNotifierMessageConverter = SlackNotifierMessageConverter(),
    ):
        self.token = token
        self.channel = channel
        self.converter = converter

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def publish(self, notifier_message: NotifierMessage):

        client = WebClient(token=self.token)

        try:
            client.chat_postMessage(
                channel=self.channel,
                blocks=self.converter.convert(notifier_message=notifier_message),
            )
        except SlackApiError as e:
            raise ConnectionError(f"SlackApiError: {e.response['error']}")
