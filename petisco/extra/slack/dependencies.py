from typing import List

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.application.notifier.not_implemented_notifier import (
    NotImplementedNotifier,
)
from petisco.extra.slack.application.notifier.slack_notifier import SlackNotifier


def get_basic_notifier_dependencies(
    token: str = None, channel: str = None
) -> List[Dependency]:

    return [
        Dependency(
            name="notifier",
            default_instance=NotImplementedNotifier(),
            envar_modifier="PETISCO_NOTIFIER_TYPE",
        )
    ]


def get_extra_notifier_dependencies(token: str, channel: str) -> List[Dependency]:

    return [
        Dependency(
            name="notifier",
            default_instance=NotImplementedNotifier(),
            envar_modifier="PETISCO_NOTIFIER_TYPE",
            instances={"slack": SlackNotifier(token=token, channel=channel)},
        )
    ]
