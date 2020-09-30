import pytest

from petisco.event.shared.domain.config_events import ConfigEvents


@pytest.fixture
def given_valid_event_config():
    """
    {'events': {'message_broker': 'rabbitmq', 'organization': 'alice', 'service': 'petisco', 'subscribers': {'UserCreated': {'version': 1, 'handlers': 'tests.application.callable_functions.handlers.send_mail_handler'}, 'UserUpdated': {'version': 1, 'handlers': ['tests.application.callable_functions.handlers.send_mail_handler', 'tests.application.callable_functions.handlers.send_sms_handler']}}}}
    :return:
    """
    return {
        "events": {
            "UserCreated": {
                "version": 1,
                "handlers": "tests.application.handlers.send_mail_handler",
            },
            "UserUpdated": {
                "version": 1,
                "handlers": [
                    "tests.application.handlers.send_mail_handler",
                    "tests.application.handlers.send_sms_handler",
                ],
            },
        }
    }


@pytest.fixture
def given_invalid_handlers_on_event_config():
    return {
        "events": {
            "UserCreated": {"version": 1, "handlers": "not.valid.send_mail_handler"},
            "UserUpdated": {
                "version": 1,
                "handlers": [
                    "tests.application.handlers.send_mail_handler",
                    "tests.application.handlers.send_sms_handler",
                ],
            },
        }
    }


@pytest.mark.unit
def test_should_load_config_event_from_valid_dictionary(given_valid_event_config):
    config_events = ConfigEvents.from_dict(given_valid_event_config)

    assert isinstance(config_events, ConfigEvents)


@pytest.mark.unit
def test_should_raise_an_error_given_invalid_handlers_on_event_config(
    given_invalid_handlers_on_event_config
):

    with pytest.raises(TypeError):
        _ = ConfigEvents.from_dict(given_invalid_handlers_on_event_config)
