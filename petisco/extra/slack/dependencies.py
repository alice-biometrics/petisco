from typing import List

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.application.notifier.not_implemented_notifier import (
    NotImplementedNotifierBuilder,
)


def get_default_notifier_dependencies() -> List[Dependency]:

    return [
        Dependency(
            name="notifier",
            default_builder=NotImplementedNotifierBuilder(),
            envar_modifier="PETISCO_NOTIFIER_TYPE",
        )
    ]


def get_slack_notifier_dependencies(token: str, channel: str) -> List[Dependency]:
    from petisco.extra.slack.application.notifier.slack_notifier import (
        SlackNotifierBuilder,
    )

    return [
        Dependency(
            name="notifier",
            default_builder=NotImplementedNotifierBuilder(),
            envar_modifier="PETISCO_NOTIFIER_TYPE",
            builders={"slack": SlackNotifierBuilder(token, channel)},
        )
    ]
