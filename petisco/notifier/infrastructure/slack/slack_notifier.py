import json
from typing import Dict

from petisco.notifier.domain.interface_notifier import INotifier
from slack import WebClient
from slack.errors import SlackApiError

from petisco.notifier.domain.notifier_message import NotifierMessage


class SlackNotifier(INotifier):
    def __init__(self, token: str, channel: str, petisco_info: Dict):
        self.token = token
        self.channel = channel
        self.petisco_info = petisco_info

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def __get_blocks(self, notifier_message: NotifierMessage):
        blocks = []
        header_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Metadata:* {json.dumps(self.petisco_info)}",
            },
        }
        divider_block = {"type": "divider"}
        message_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Message:* {notifier_message.message}",
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
