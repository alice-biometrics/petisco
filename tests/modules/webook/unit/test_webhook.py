import pytest

from petisco import Webhook
from petisco.webhooks.webhook.domain.invalid_url_error import InvalidUrlError
from petisco.webhooks.webhook.domain.webhook_created import WebhookCreated
from tests.modules.webook.mothers.webhook_mother import WebhookMother


@pytest.mark.unit
def test_should_construct_a_valid_webhook():
    webhook = WebhookMother.default()
    assert isinstance(webhook, Webhook)
    assert isinstance(webhook.pull_domain_events()[0], WebhookCreated)


@pytest.mark.unit
def test_should_raise_an_error_when_construct_a_webhook_with_invalid_url():

    with pytest.raises(InvalidUrlError):
        WebhookMother.with_invalid_url()


@pytest.mark.unit
def test_should_serialize_successfully():
    original_webhook = WebhookMother.default()
    webhook_data = original_webhook.to_dict()
    retrieved_webhook = Webhook.from_dict(webhook_data)
    assert original_webhook == retrieved_webhook


@pytest.mark.unit
def test_should_check_active_attribute_on_webhooks():
    assert WebhookMother.default().active
    assert not WebhookMother.not_active().active
