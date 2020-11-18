import pytest
import requests_mock
from meiga.assertions import assert_success

from petisco.webhooks.webhook.domain.webhook_result import WebhookResult
from tests.modules.webook.mothers.webhook_mother import WebhookMother, DEFAULT_POST_URL
from tests.modules.webook.mothers.webhook_sender_mother import WebhookSenderMother


@pytest.mark.integration
def test_should_be_failure_when_ping_a_webhook_and_url_is_not_reachable():
    webhook = WebhookMother.default()
    sender = WebhookSenderMother.default()

    result = sender.ping(webhook)

    assert_success(result, value_is_instance_of=WebhookResult)

    webhook_result = result.value
    assert not webhook_result.is_success


@pytest.mark.integration
def test_should_be_failure_when_execute_a_webhook_and_url_is_not_reachable():
    webhook = WebhookMother.default()
    sender = WebhookSenderMother.default()

    result = sender.execute(webhook, {"payload": "ok"})

    assert_success(result, value_is_instance_of=WebhookResult)

    webhook_result = result.value
    assert not webhook_result.is_success


@pytest.mark.integration
def test_should_be_success_when_ping_a_webhook_and_url_is_reachable_by_mocking_it():
    webhook = WebhookMother.default()
    sender = WebhookSenderMother.default()

    with requests_mock.Mocker() as m:
        m.post(DEFAULT_POST_URL)
        result = sender.ping(webhook)
        webhook_result = result.value
        assert webhook_result.is_success


@pytest.mark.integration
def test_should_be_success_when_execute_a_webhook_and_url_is_reachable_by_mocking_it():
    webhook = WebhookMother.default()
    sender = WebhookSenderMother.default()

    with requests_mock.Mocker() as m:
        m.post(DEFAULT_POST_URL)
        result = sender.execute(webhook, {"payload": "ok"})
        webhook_result = result.value
        assert webhook_result.is_success
