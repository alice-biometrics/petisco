import pytest
import requests_mock
from meiga.assertions import assert_failure, assert_success

from petisco import ConnectionRequestError, Response
from tests.modules.webook.mothers.webhook_mother import WebhookMother, DEFAULT_POST_URL


@pytest.mark.integration
def test_should_be_failure_when_ping_a_webhook_and_url_is_not_reachable():
    webhook = WebhookMother.default()
    result = webhook.ping()
    assert_failure(result, value_is_instance_of=ConnectionRequestError)


@pytest.mark.integration
def test_should_be_failure_when_execute_a_webhook_and_url_is_not_reachable():
    webhook = WebhookMother.default()
    result = webhook.execute({"payload": "ok"})
    assert_failure(result, value_is_instance_of=ConnectionRequestError)


@pytest.mark.integration
def test_should_be_success_when_ping_a_webhook_and_url_is_reachable_by_mocking_it():
    webhook = WebhookMother.default()
    with requests_mock.Mocker() as m:
        m.post(DEFAULT_POST_URL)
        result = webhook.ping()
        assert_success(result, value_is_instance_of=Response)


@pytest.mark.integration
def test_should_be_success_when_execute_a_webhook_and_url_is_reachable_by_mocking_it():
    webhook = WebhookMother.default()
    with requests_mock.Mocker() as m:
        m.post(DEFAULT_POST_URL)
        result = webhook.execute({"payload": "ok"})
        assert_success(result, value_is_instance_of=Response)
