from typing import Dict

from petisco.domain.aggregate_roots.info_id import InfoId
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

    def __info_block(self, info_id: InfoId):
        if not info_id:
            return None
        info_id_text = f":information_source: *Info*\n"
        info_id_available = False
        if info_id.client_id:
            info_id_text += f"*Client:* {info_id.client_id}\n"
            info_id_available = True
        if info_id.user_id:
            info_id_text += f"*UserID:* {info_id.user_id}\n"
            info_id_available = True
        if info_id.correlation_id:
            info_id_text += f"*CorrelationID:* {info_id.correlation_id}\n"
            info_id_available = True
        if info_id.correlation_id:
            info_id_text += f"*IP:* {info_id.ip}"
            info_id_available = True
        if not info_id_available:
            return None
        return {
            "type": "section",
            "text": {"type": "mrkdwn", "text": info_id_text},
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
        info_id_block = self.__info_block(notifier_message.info_id)

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
        if info_id_block:
            blocks.append(info_id_block)
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
            raise ConnectionError(f"SlackApiError: {e.response['error']}")
