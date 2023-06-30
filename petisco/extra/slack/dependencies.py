from typing import List

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.application.notifier.not_implemented_notifier import (
    NotImplementedNotifier,
)
from petisco.base.application.notifier.notifier import Notifier
from petisco.base.misc.builder import Builder


def get_default_notifier_dependencies() -> List[Dependency]:
    return [
        Dependency(
            Notifier,
            builders={"default": Builder(NotImplementedNotifier)},
            envar_modifier="PETISCO_NOTIFIER_TYPE",
        )
    ]


def get_slack_notifier_dependencies(token: str, channel: str) -> List[Dependency]:
    from petisco.extra.slack.application.notifier.slack_notifier import SlackNotifier

    return [
        Dependency(
            Notifier,
            builders={
                "default": Builder(SlackNotifier, token=token, channel=channel),
                "not_implemented": Builder(NotImplementedNotifier),
            },
            envar_modifier="PETISCO_NOTIFIER_TYPE",
        )
    ]
