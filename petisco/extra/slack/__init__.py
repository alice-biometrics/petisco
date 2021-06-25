__all__ = []

from petisco.extra.slack.is_slack_available import is_slack_available

slack = []
if is_slack_available():
    from petisco.extra.slack.application.notifier.slack_notifier import SlackNotifier
    from petisco.extra.slack.application.notifier.slack_notifier_message_converter import (
        SlackNotifierMessageConverter,
    )
    from petisco.extra.slack.dependencies import get_slack_notifier_dependencies

    slack = [
        "SlackNotifier",
        "SlackNotifierMessageConverter",
        "get_slack_notifier_dependencies",
    ]
else:
    from petisco.extra.slack.dependencies import get_basic_notifier_dependencies

    slack = ["get_basic_notifier_dependencies"]


__all__ = slack
