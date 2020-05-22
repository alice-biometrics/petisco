from typing import Dict

from petisco.notifier.domain.interface_notifier import INotifier
from slack import WebClient
from slack.errors import SlackApiError

from petisco.notifier.domain.notifier_exception_message import NotifierExceptionMessage
from petisco.notifier.domain.notifier_message import NotifierMessage


class SlackNotifier(INotifier):
    def __init__(self, token: str, channel: str, petisco_info: Dict):
        self.token = token
        self.channel = channel
        self.petisco_info = petisco_info

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def __header_block(self):
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":cookie: *Message from Petisco*\n*Application:* {self.petisco_info['app_name']} ({self.petisco_info['app_version']})\n*Petisco:* {self.petisco_info['petisco_version']}",
            },
        }

    def __get_blocks_exception_message(
        self, notifier_message: NotifierExceptionMessage
    ):
        blocks = []
        header_block = self.__header_block()
        divider_block = {"type": "divider"}
        exception_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":fire: *Exception* \n*Class*: {notifier_message.exception.__class__} *Description:* {notifier_message.exception}",
            },
        }
        function_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":pushpin: *Function*\n{notifier_message.function}",
            },
        }
        traceback_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":scroll: *Traceback*\n{notifier_message.traceback}",
            },
        }
        blocks.append(header_block)
        blocks.append(divider_block)
        blocks.append(exception_block)
        blocks.append(function_block)
        blocks.append(traceback_block)
        return blocks

    def __get_blocks(self, notifier_message: NotifierMessage):
        if isinstance(notifier_message, NotifierExceptionMessage):
            blocks = self.__get_blocks_exception_message(notifier_message)
        else:
            blocks = []
            header_block = self.__header_block()
            divider_block = {"type": "divider"}
            message_block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":envelope: *Message*\n{notifier_message.message}",
                },
            }
            blocks.append(header_block)
            blocks.append(divider_block)
            blocks.append(message_block)
        return blocks

    def publish(self, notifier_message: NotifierMessage):

        client = WebClient(token=self.token)

        try:
            client.chat_postMessage(
                channel=self.channel, blocks=self.__get_blocks(notifier_message)
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")
