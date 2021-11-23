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
    @staticmethod
    def get_slack_notifier():
        slack_token = os.getenv("SLACK_TOKEN")
        slack_tests_channel = os.getenv("SLACK_TESTS_CHANNEL")
        return SlackNotifier(token=slack_token, channel=slack_tests_channel)

    def test_publish_should_send_notification(self):
        notifier = self.get_slack_notifier()
        notifier_message = NotifierMessage(title="Test title", message="test message")
        notifier.publish(notifier_message=notifier_message)

    def test_publish_exception_should_send_notification(self):
        notifier = self.get_slack_notifier()
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
            notifier.publish_exception(
                notifier_exception_message=notifier_exception_message
            )
