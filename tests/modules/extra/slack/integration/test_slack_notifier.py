import os

import pytest

from petisco import NotifierExceptionMessage, NotifierMessage, UnknownError
from petisco.extra.slack import SlackNotifier

LONG_TEXT = "long_text" * 1000


@pytest.mark.skipif(
    condition=os.getenv("SLACK_TOKEN") is None,
    reason="Slack token is a github secret only available in CI workflows",
)
@pytest.mark.integration
class TestSlackNotifier:
    def setup(self):
        slack_token = os.getenv("SLACK_TOKEN")
        slack_tests_channel = os.getenv("SLACK_TESTS_CHANNEL")
        self.notifier = SlackNotifier(token=slack_token, channel=slack_tests_channel)

    def should_success_when_publish_notification(self):
        notifier_message = NotifierMessage(title="Test title", message="test message")
        self.notifier.publish(notifier_message=notifier_message)

    def should_success_when_publish_exception_notification(self):
        try:
            raise Exception(LONG_TEXT)
        except Exception as exception:
            error = UnknownError.from_exception(
                exception=exception, arguments={"param": LONG_TEXT}
            )
            notifier_exception_message = NotifierExceptionMessage.from_unknown_error(
                unknown_error=error, title="Test title error"
            )
            notifier_exception_message.traceback += LONG_TEXT
            self.notifier.publish_exception(
                notifier_exception_message=notifier_exception_message
            )
