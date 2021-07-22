from typing import Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from petisco.base.application.notifier.notifier import Notifier
from petisco.base.application.notifier.notifier_exception_message import (
    NotifierExceptionMessage,
)
from petisco.base.application.notifier.notifier_message import NotifierMessage
from petisco.base.domain.errors.domain_error import DomainError
from petisco.extra.slack.application.notifier.blocks_slack_notifier_message_converter import (
    BlocksSlackNotifierMessageConverter,
    SlackNotifierMessageConverter,
)
from petisco.extra.slack.application.notifier.exception_blocks_slack_notifier_message_converter import (
    ExceptionBlocksSlackNotifierMessageConverter,
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
        exception_converter: Optional[
            SlackNotifierMessageConverter
        ] = ExceptionBlocksSlackNotifierMessageConverter(),
    ):
        self.channel = channel
        self.converter = converter
        self.exception_converter = exception_converter
        self.client = WebClient(token=token)

    def publish(self, notifier_message: NotifierMessage):
        try:
            self.client.chat_postMessage(
                channel=self.channel,
                blocks=self.converter.convert(notifier_message),
                text=notifier_message.title,
            )
        except SlackApiError as e:
            raise SlackError(e.response["error"])

    def publish_exception(self, notifier_exception_message: NotifierExceptionMessage):
        try:
            self.client.chat_postMessage(
                channel=self.channel,
                blocks=self.exception_converter.convert(notifier_exception_message),
                text=notifier_exception_message.title,
            )
        except SlackApiError as e:
            raise SlackError(e.response["error"])
