import os
from typing import Optional, Callable

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)
from petisco.notifier.infrastructure.not_implemented_notifier import (
    NotImplementedNotifier,
)
from petisco.notifier.infrastructure.slack.slack_notifier_message_converter import (
    SlackNotifierMessageConverter,
)
from petisco.notifier.infrastructure.slack.slack_notifier import SlackNotifier


def get_slack_notifier():
    slack_token = os.environ.get("SLACK_API_TOKEN", None)
    slack_channel = os.environ.get("SLACK_CHANNEL", "#feed")
    if not slack_token:
        raise ConnectionError(
            "Petisco Slack Notifier is not configured. "
            "Please check Slack Notifier configuration and add required values"
        )
    return SlackNotifier(
        token=slack_token,
        channel=slack_channel,
        converter=SlackNotifierMessageConverter(),
    )


def get_default_notifier():
    return NotImplementedNotifier()


@dataclass
class ConfigNotifier:
    provider: Optional[Callable] = None

    @staticmethod
    def from_dict(kdict):
        provider = get_default_notifier
        if kdict and isinstance(kdict, dict):
            provider = (
                get_function_from_string(kdict.get("provider"))
                .handle(
                    on_failure=raise_petisco_config_exception,
                    failure_args=(kdict, "notifier:provider"),
                )
                .unwrap()
            )

        return ConfigNotifier(provider=provider)
