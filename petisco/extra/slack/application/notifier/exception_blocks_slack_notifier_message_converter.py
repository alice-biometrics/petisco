from typing import Dict

from petisco.base.application.notifier.notifier_exception_message import (
    NotifierExceptionMessage,
)
from petisco.extra.slack.application.notifier.create_text_meta import create_text_meta
from petisco.extra.slack.application.notifier.slack_notifier_message_converter import (
    SlackNotifierMessageConverter,
)


class ExceptionBlocksSlackNotifierMessageConverter(SlackNotifierMessageConverter):
    def __init__(
        self,
        slack_accessory: Dict = None,
        repository_url: str = None,
        repository_name_button: str = "Code",
    ):
        self.slack_accessory = slack_accessory
        self.repository_url = repository_url
        self.repository_name_button = repository_name_button

    def _create_header_block(self, title: str):
        return {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": title,
                "emoji": True,
            },
        }

    def _create_message_block(
        self, notifier_exception_message: NotifierExceptionMessage
    ):
        text_meta = create_text_meta(notifier_exception_message.meta)
        message_block = None
        if text_meta:
            message_block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text_meta,
                },
            }
            if self.slack_accessory:
                message_block["accessory"] = self.slack_accessory
        return message_block

    def _create_executor_block(
        self, notifier_exception_message: NotifierExceptionMessage
    ):
        executor_block = {
            "type": "section",
        }

        if self.repository_url:
            url_error = f"{self.repository_url}/{notifier_exception_message.filename}"
            if notifier_exception_message.lineno:
                url_error += f"#L{notifier_exception_message.lineno}"
            executor_block["accessory"] = {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": self.repository_name_button,
                    "emoji": True,
                },
                "value": "click_me_repository_code",
                "url": url_error,
                "action_id": "button-repository-code",
                "style": "danger",
            }

        text_executor = f"*Executor*: {notifier_exception_message.executor}"
        if notifier_exception_message.filename:
            text_executor += f"\n {notifier_exception_message.filename}"
        if notifier_exception_message.lineno:
            text_executor += f" | Line {notifier_exception_message.lineno}"

        if notifier_exception_message.input_parameters:
            input_parameters_text = ""
            for k, v in notifier_exception_message.input_parameters.items():
                input_parameters_text += f"\n>{k}: {v}"
            text_executor += input_parameters_text[: 3000 - len(text_executor)]

        executor_block["text"] = {
            "type": "mrkdwn",
            "text": text_executor,
        }
        return executor_block

    def _create_error_block(self, notifier_exception_message: NotifierExceptionMessage):
        error_block = None
        if notifier_exception_message.exception:
            text_error = (
                f"*Class*: {notifier_exception_message.exception.__class__}\n"
                f">{str(notifier_exception_message.exception)[:500]}"
            )
            traceback_base_str = "\n```{}```"
            traceback_max_length = 3000 - len(text_error) - len(traceback_base_str)
            text_error += traceback_base_str.format(
                notifier_exception_message.traceback[:traceback_max_length]
            )

            error_block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text_error,
                },
            }
        return error_block

    def convert(self, notifier_exception_message: NotifierExceptionMessage):

        blocks = []
        header_block = self._create_header_block(notifier_exception_message.title)
        message_block = self._create_message_block(notifier_exception_message)
        executor_block = self._create_executor_block(notifier_exception_message)
        error_block = self._create_error_block(notifier_exception_message)

        blocks.append(header_block)
        if message_block:
            blocks.append(message_block)
        blocks.append(executor_block)

        if error_block:
            blocks.append(error_block)

        divider_block = {"type": "divider"}
        blocks.append(divider_block)

        return blocks
