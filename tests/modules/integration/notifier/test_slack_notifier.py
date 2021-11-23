import os

import pytest
from petisco import NotifierMessage
from petisco.notifier.domain.notifier_exception_message import NotifierExceptionMessage
from petisco.notifier.infrastructure.slack.slack_notifier import SlackNotifier
from tests.modules.shared.info_id_mother import InfoIdMother

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
        import traceback

        notifier = self.get_slack_notifier()
        try:
            raise Exception(LONG_TEXT)
        except Exception as exception:
            notifier_exception_message = NotifierExceptionMessage(
                exception=exception,
                input_parameters={"key": LONG_TEXT},
                executor="executor",
                traceback=traceback.format_exc() + LONG_TEXT,
                info_id=InfoIdMother.random(),
                info_petisco={},
            )
            notifier.publish(notifier_message=notifier_exception_message)
