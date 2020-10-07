import pytest

from petisco.event.shared.domain.config_events import ConfigEvents


@pytest.fixture
def given_valid_event_config():
    return {
        "events": {
            "message_broker": "not_implemented",
            "organization": "alice",
            "service": "petisco",
            "subscribers": {
                "UserCreated": {
                    "version": 1,
                    "handlers": "tests.modules.event.unit.callable_functions.handlers.send_mail_handler",
                },
                "UserUpdated": {
                    "version": 1,
                    "handlers": [
                        "tests.modules.event.unit.callable_functions.handlers.send_mail_handler",
                        "tests.modules.event.unit.callable_functions.handlers.send_sms_handler",
                    ],
                },
            },
        }
    }


@pytest.fixture
def given_invalid_handlers_on_event_config():
    return {
        "events": {
            "message_broker": "not_implemented",
            "organization": "alice",
            "service": "petisco",
            "subscribers": {
                "UserCreated": {
                    "version": 1,
                    "handlers": "not.valid.handlers.send_mail_handler",
                },
                "UserUpdated": {
                    "version": 1,
                    "handlers": [
                        "tests.modules.event.unit.callable_functions.handlers.send_mail_handler",
                        "tests.modules.event.unit.callable_functions.handlers.send_sms_handler",
                    ],
                },
            },
        }
    }


@pytest.fixture
def given_valid_event_config_with_queue_subscribers():
    return {
        "events": {
            "message_broker": "not_implemented",
            "organization": "alice",
            "service": "petisco",
            "subscribers": {
                "UserCreated": {
                    "version": 1,
                    "handlers": "tests.modules.event.unit.callable_functions.handlers.send_mail_handler",
                },
                "UserUpdated": {
                    "version": 1,
                    "handlers": [
                        "tests.modules.event.unit.callable_functions.handlers.send_mail_handler",
                        "tests.modules.event.unit.callable_functions.handlers.send_sms_handler",
                    ],
                },
            },
        },
        "queues": {
            "store": "tests.modules.event.unit.callable_functions.handlers.event_store",
            "subscribers": {
                "dead_letter.store": "tests.modules.event.unit.callable_functions.handlers.requeue_event"
            },
        },
    }


@pytest.mark.unit
def test_should_load_config_event_from_valid_dictionary(given_valid_event_config):
    config_events = ConfigEvents.from_dict(given_valid_event_config)

    assert isinstance(config_events, ConfigEvents)


@pytest.mark.unit
def test_should_load_config_event_from_valid_dictionary_with_queue_subscribers(
    given_valid_event_config_with_queue_subscribers
):
    config_events = ConfigEvents.from_dict(
        given_valid_event_config_with_queue_subscribers
    )

    assert isinstance(config_events, ConfigEvents)


@pytest.mark.unit
def test_should_raise_an_error_given_invalid_handlers_on_event_config(
    given_invalid_handlers_on_event_config
):

    with pytest.raises(TypeError):
        _ = ConfigEvents.from_dict(given_invalid_handlers_on_event_config)
