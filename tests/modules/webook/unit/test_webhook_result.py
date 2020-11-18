import pytest

from petisco import WebhookSenderFailed
from petisco.webhooks.webhook.domain.webhook_result import WebhookResult
from tests.modules.webook.mothers.webhook_result_mother import WebhookResultMother


@pytest.mark.unit
@pytest.mark.parametrize(
    "webhook_result",
    [
        WebhookResultMother.success(),
        WebhookResultMother.failure(),
        WebhookResultMother.without_response(),
        WebhookResultMother.without_request(),
        WebhookResultMother.without_request_headers(),
    ],
)
def test_should_serialize_and_deserialize_a_webhook_result(webhook_result):
    serialized = webhook_result.to_dict()

    deserialized_webhook_result = WebhookResult.from_dict(serialized)

    assert webhook_result == deserialized_webhook_result


@pytest.mark.unit
def test_should_check_not_events_when_success():
    webhook_result = WebhookResultMother.success_from_create()
    assert len(webhook_result.pull_domain_events()) == 0


@pytest.mark.unit
def test_should_check_webhook_sender_failed_event_when_is_failure():
    webhook_result = WebhookResultMother.failure_from_create()
    assert len(webhook_result.pull_domain_events()) == 1
    assert isinstance(webhook_result.pull_first_domain_event(), WebhookSenderFailed)
