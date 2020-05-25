import json
from unittest.mock import patch, MagicMock

import pytest
from slack import WebClient

from petisco.notifier.domain.notifier_message import NotifierMessage
from petisco.notifier.infrastructure.slack.slack_notifier import SlackNotifier


@pytest.mark.integration
@patch.object(WebClient, "chat_postMessage")
def test_should_publish_a_notifier_message(mock_slack_client):

    notifier = SlackNotifier(token="test_token", channel="#feed")
    notifier.publish(NotifierMessage(message="Test message"))
    mock_slack_client.return_value = MagicMock(
        status_code=200, response=json.dumps({"key": "value"})
    )
    mock_slack_client.assert_called_once()
