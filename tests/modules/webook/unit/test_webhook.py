import pytest

from petisco import Webhook
from petisco.webhooks.webhook.domain.invalid_url_error import InvalidUrlError
from tests.modules.webook.mothers.webhook_mother import WebhookMother


@pytest.mark.unit
def test_should_construct_a_valid_webhook():
    webhook = WebhookMother.default()
    assert isinstance(webhook, Webhook)


@pytest.mark.unit
def test_should_raise_an_error_when_construct_a_webhook_with_invalid_url():

    with pytest.raises(InvalidUrlError):
        WebhookMother.with_invalid_url()
