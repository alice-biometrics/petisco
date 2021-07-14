from typing import List

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.application.notifier.not_implemented_notifier import (
    NotImplementedNotifier,
)


def get_default_notifier_dependencies() -> List[Dependency]:

    return [
        Dependency(
            name="notifier",
            default_instance=NotImplementedNotifier(),
            envar_modifier="PETISCO_NOTIFIER_TYPE",
        )
    ]


def get_slack_notifier_dependencies(token: str, channel: str) -> List[Dependency]:
    from petisco.extra.slack.application.notifier.slack_notifier import SlackNotifier

    return [
        Dependency(
            name="notifier",
            default_instance=NotImplementedNotifier(),
            envar_modifier="PETISCO_NOTIFIER_TYPE",
            instances={"slack": SlackNotifier(token=token, channel=channel)},
        )
    ]
