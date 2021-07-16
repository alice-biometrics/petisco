from typing import Optional

from slack import WebClient
from slack.errors import SlackApiError

from petisco.base.application.notifier.notifier import Notifier
from petisco.base.application.notifier.notifier_message import NotifierMessage
from petisco.base.domain.errors.domain_error import DomainError
from petisco.base.misc.builder import Builder
from petisco.extra.slack.application.notifier.blocks_slack_notifier_message_converter import (
    BlocksSlackNotifierMessageConverter,
    SlackNotifierMessageConverter,
)


class SlackError(DomainError):
    pass


class SlackNotifier(Notifier):
    def __init__(
        self,
        token: str,
        channel: str,
        converter: Optional[
            SlackNotifierMessageConverter
        ] = BlocksSlackNotifierMessageConverter(),
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


class SlackNotifierBuilder(Builder):
    def __init__(self, token: str, channel: str):
        self.token = token
        self.channel = channel

    def build(self) -> SlackNotifier:
        return SlackNotifier(self.token, self.channel)
