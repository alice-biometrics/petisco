import json

import pytest
from requests.structures import CaseInsensitiveDict
from petisco.webhooks.webhook.domain.webhook_response_result import (
    WebhookResponseResult,
)


@pytest.mark.unit
def test_should_construct_and_convert_to_dict_webhook_response_result_from_case_insensitive_dict_headers():

    expected_headers = {
        "X-Petisco-Event": "user_created",
        "X-Petisco-Event-Version": "1",
        "X-Petisco-Delivery": "a026531a-8512-4599-9491-81909ea8e31b",
        "X-Petisco-WebhookId": "1baa14dc-bda9-400f-b45b-428f26532f1d",
        "X-Petisco-Request-Timestamp": "2020-11-18 11:38:37.156162",
        "User-Agent": "Petisco-Hookshoot/",
        "apikey": "'b0b905d6-228f-44bf-a130-c85d7aecd765",
    }
    headers = CaseInsensitiveDict(expected_headers)
    body = {"payload": "ok"}
    status_code = 200
    webhook_response_result = WebhookResponseResult(
        headers=headers, body=body, status_code=status_code
    )

    assert webhook_response_result.to_dict() == {
        "headers": json.dumps(expected_headers),
        "body": json.dumps(body),
        "status_code": status_code,
        "completed_in_ms": None,
    }


@pytest.mark.unit
def test_should_construct_and_convert_to_dict_webhook_response_result_from_default_dicts():

    headers = {
        "X-Petisco-Event": "user_created",
        "X-Petisco-Event-Version": "1",
        "X-Petisco-Delivery": "a026531a-8512-4599-9491-81909ea8e31b",
        "X-Petisco-WebhookId": "1baa14dc-bda9-400f-b45b-428f26532f1d",
        "X-Petisco-Request-Timestamp": "2020-11-18 11:38:37.156162",
        "User-Agent": "Petisco-Hookshoot/",
        "apikey": "'b0b905d6-228f-44bf-a130-c85d7aecd765",
    }
    body = {"payload": "ok"}
    status_code = 200
    completed_in_ms = 80

    webhook_response_result = WebhookResponseResult(
        headers=headers,
        body=body,
        status_code=status_code,
        completed_in_ms=completed_in_ms,
    )

    assert webhook_response_result.to_dict() == {
        "headers": json.dumps(headers),
        "body": json.dumps(body),
        "status_code": status_code,
        "completed_in_ms": completed_in_ms,
    }
