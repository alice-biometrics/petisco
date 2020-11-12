import pytest

from petisco.event.queue.domain.specific_queue_config import SpecificQueueConfig


@pytest.mark.unit
@pytest.mark.parametrize(
    "queue_name,wildcard,expected_result",
    [
        ("petisco.service.1.event.user_created", "*send_webhook*", False),
        (
            "petisco.service.1.event.user_created.send_webhook_on_user_created",
            "*send_webhook*",
            True,
        ),
        (
            "petisco.service.1.event.user_created.send_webhook_on_user_created",
            "send_webhook*",
            False,
        ),
    ],
)
def test_should_queue_config_works_as_expected(queue_name, wildcard, expected_result):

    specific_queue_config = SpecificQueueConfig(wildcard=wildcard)

    assert specific_queue_config.has_specific_config(queue_name) == expected_result


@pytest.mark.unit
def test_should_queue_config_works_as_expected_with_specific_parameters():
    specific_queue_config = SpecificQueueConfig(
        wildcard="*send_webhook*", specific_retry_ttl=10, specific_main_ttl=20
    )
    assert specific_queue_config.get_retry_ttl() == 10
    assert specific_queue_config.get_main_ttl() == 20


@pytest.mark.unit
@pytest.mark.parametrize(
    "queue_name,queue_config_dict,expected_result",
    [
        (
            "petisco.service.1.event.user_created",
            {
                "when_queue_contains": "*send_webhook*",
                "use": {"retry_ttl": 1, "main_ttl": 1},
            },
            False,
        ),
        (
            "petisco.service.1.event.user_created.send_webhook_on_user_created",
            {
                "when_queue_contains": "*send_webhook*",
                "use": {"retry_ttl": 1, "main_ttl": 1},
            },
            True,
        ),
        (
            "petisco.service.1.event.user_created.send_webhook_on_user_created",
            {"when_queue_contains": "*send_webhook*", "use": {"retry_ttl": 1}},
            True,
        ),
    ],
)
def test_should_queue_config_works_as_expected_when_load_from_dict(
    queue_name, queue_config_dict, expected_result
):

    specific_queue_config = SpecificQueueConfig.from_dict(
        queue_config_dict, default_retry_ttl=10, default_main_ttl=20
    )

    assert specific_queue_config.has_specific_config(queue_name) == expected_result
