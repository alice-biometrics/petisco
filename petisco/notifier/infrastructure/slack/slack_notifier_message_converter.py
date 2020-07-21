from typing import List, Dict, Optional

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.notifier.domain.notifier_exception_message import NotifierExceptionMessage
from petisco.notifier.domain.notifier_message import NotifierMessage
from petisco.notifier.infrastructure.slack.interface_slack_notifier_message_converter import (
    ISlackNotifierMessageConverter,
)


class SlackNotifierMessageConverter(ISlackNotifierMessageConverter):
    def __repr__(self):
        return super().__repr__()

    def __info_petisco_block(self, info_petisco: Dict) -> Dict:
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":cookie: *Message from Petisco*\n*Application:* {info_petisco['app_name']} ({info_petisco['app_version']})\n*Petisco:* {info_petisco['petisco_version']}\n*Environment:* {info_petisco['environment']}",
            },
        }

    def _info_id_block(self, info_id: InfoId) -> Optional[Dict]:
        if not info_id:
            return None
        info_id_text = f":information_source: *InfoId*\n"
        info_id_available = False
        if info_id.client_id:
            info_id_text += f"*ClientId:* {info_id.client_id.value}\n"
            info_id_available = True
        if info_id.user_id:
            info_id_text += f"*UserId:* {info_id.user_id.value}\n"
            info_id_available = True
        if info_id.correlation_id:
            info_id_text += f"*CorrelationId:* {info_id.correlation_id.value}\n"
            info_id_available = True
        if info_id.correlation_id:
            info_id_text += f"*IP:* {info_id.ip}"
            info_id_available = True
        if not info_id_available:
            return None
        return {"type": "section", "text": {"type": "mrkdwn", "text": info_id_text}}

    def __get_common_blocks(self, notifier_message: NotifierMessage) -> List[Dict]:
        blocks = []
        if notifier_message.info_petisco:
            blocks.append(self.__info_petisco_block(notifier_message.info_petisco))
        if notifier_message.info_id:
            blocks.append(self._info_id_block(notifier_message.info_id))
        if len(blocks) > 0:
            blocks.append({"type": "divider"})
        return blocks

    def __get_blocks_exception_message(
        self, notifier_message: NotifierExceptionMessage
    ) -> List[Dict]:
        blocks = []

        exception_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":fire: *Exception* \n*Class*: {notifier_message.exception.__class__} *Description:* {notifier_message.exception}",
            },
        }
        executor_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":pushpin: *Executor*\n{notifier_message.executor}",
            },
        }

        input_parameters_block_text = f":arrow_right: *Input Parameters*\n"

        if notifier_message.input_parameters:
            for k, v in notifier_message.input_parameters.items():
                input_parameters_block_text += f"* {k}: {v}\n"
        else:
            input_parameters_block_text += "No data :heavy_multiplication_x:"

        input_parameters_block = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": input_parameters_block_text},
        }
        traceback_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":scroll: *Traceback*\n```{notifier_message.traceback[:2500]}```",
            },
        }
        blocks += self.__get_common_blocks(notifier_message)
        blocks.append(exception_block)
        blocks.append(executor_block)
        blocks.append(input_parameters_block)
        blocks.append(traceback_block)
        return blocks

    def convert(self, notifier_message: NotifierMessage):
        if isinstance(notifier_message, NotifierExceptionMessage):
            blocks = self.__get_blocks_exception_message(notifier_message)
        else:
            blocks = []
            message_block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":envelope: *Message*\n{notifier_message.message}",
                },
            }
            blocks += self.__get_common_blocks(notifier_message)
            if notifier_message.title:
                title_block = {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":label: *Title*\n{notifier_message.title}",
                    },
                }
                blocks.append(title_block)
            blocks.append(message_block)
        return blocks
