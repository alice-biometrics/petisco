from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from petisco.legacy.notifier.domain.interface_notifier import INotifier
from petisco.legacy.notifier.domain.notifier_message import NotifierMessage
from petisco.legacy.notifier.infrastructure.slack.errors import SlackError
from petisco.legacy.notifier.infrastructure.slack.interface_slack_notifier_message_converter import (
    ISlackNotifierMessageConverter,
)
from petisco.legacy.notifier.infrastructure.slack.slack_notifier_message_converter import (
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

    def publish(self, notifier_message: NotifierMessage):

        client = WebClient(token=self.token)

        try:
            client.chat_postMessage(
                channel=self.channel,
                blocks=self.converter.convert(notifier_message=notifier_message),
            )
        except SlackApiError as e:
            raise SlackError(e.response["error"])
