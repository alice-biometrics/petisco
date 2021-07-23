from typing import Dict

from petisco.base.application.notifier.notifier_message import NotifierMessage
from petisco.extra.slack.application.notifier.create_text_meta import create_text_meta
from petisco.extra.slack.application.notifier.slack_notifier_message_converter import (
    SlackNotifierMessageConverter,
)


class BlocksSlackNotifierMessageConverter(SlackNotifierMessageConverter):
    def __init__(self, slack_accessory: Dict = None):
        self.slack_accessory = slack_accessory

    def convert(self, notifier_message: NotifierMessage):
        header_block = self._create_header_block(notifier_message.title)
        message_block = self._create_message_block(notifier_message)
        divider_block = {"type": "divider"}
        return [header_block, message_block, divider_block]

    def _create_header_block(self, title: str):
        return {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": title,
                "emoji": True,
            },
        }

    def _create_message_block(self, notifier_message: NotifierMessage):
        text_message = ""
        if notifier_message.message:
            text_message += f"{notifier_message.message}"

        text_meta = create_text_meta(notifier_message.meta)
        if text_meta:
            text_message += text_meta
        message_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text_message,
            },
        }

        if self.slack_accessory:
            message_block["accessory"] = self.slack_accessory

        return message_block
