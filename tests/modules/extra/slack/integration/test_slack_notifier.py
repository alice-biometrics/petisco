import json
from unittest.mock import MagicMock, patch

import pytest
from slack_sdk import WebClient

from petisco.extra.slack import SlackNotifier
from tests.modules.extra.slack.mother.notifier_exception_message_mother import (
    NotifierExceptionMessageMother,
)
from tests.modules.extra.slack.mother.notifier_message_mother import (
    NotifierMessageMother,
)


@pytest.mark.integration
@patch.object(WebClient, "chat_postMessage")
def test_slack_notifier_should_publish_a_notifier_message(mock_slack_client):
    notifier = SlackNotifier(token="test_token", channel="#feed")
    notifier.publish(NotifierMessageMother.any())
    mock_slack_client.return_value = MagicMock(
        status_code=200, response=json.dumps({"key": "value"})
    )
    mock_slack_client.assert_called_once()


@pytest.mark.integration
@patch.object(WebClient, "chat_postMessage")
def test_slack_notifier_should_publish_a_notifier_exception_message(mock_slack_client):
    notifier = SlackNotifier(token="test_token", channel="#feed")
    notifier.publish_exception(NotifierExceptionMessageMother.any())
    mock_slack_client.return_value = MagicMock(
        status_code=200, response=json.dumps({"key": "value"})
    )
    mock_slack_client.assert_called_once()
