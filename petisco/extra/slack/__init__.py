__all__ = []

from petisco.extra.slack.is_slack_available import is_slack_available

slack = []
if is_slack_available():
    from petisco.extra.slack.dependencies import (
        get_extra_notifier_dependencies as get_available_notifier_dependencies,
    )
    from petisco.extra.slack.application.notifier.slack_notifier import SlackNotifier
    from petisco.extra.slack.application.notifier.slack_notifier_message_converter import (
        SlackNotifierMessageConverter,
    )

    slack = [
        "get_available_notifier_dependencies",
        "SlackNotifier",
        "SlackNotifierMessageConverter",
    ]
else:
    from petisco.extra.slack.dependencies import (
        get_basic_notifier_dependencies as get_available_notifier_dependencies,
    )

    slack = ["get_available_notifier_dependencies"]


__all__ = slack
