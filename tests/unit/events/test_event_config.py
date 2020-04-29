import pytest

from petisco import EventConfig
from petisco.events.event_config import (
    EVENT_PUBLISHER_DEFAULT,
    EVENT_ADDITIONAL_DEFAULT,
)
from tests.unit.mocks.fake_event_publisher import FakeEventPublisher


@pytest.mark.unit
def test_should_check_default_event_config_is_non_configured():

    event_config = EventConfig()

    assert not event_config.is_configured


@pytest.mark.unit
@pytest.mark.parametrize(
    "event_publisher,event_additional_info",
    [
        (FakeEventPublisher(), EVENT_ADDITIONAL_DEFAULT),
        (EVENT_PUBLISHER_DEFAULT, EVENT_ADDITIONAL_DEFAULT),
        (EVENT_PUBLISHER_DEFAULT, ["user_id"]),
        (EVENT_PUBLISHER_DEFAULT, ["user_id"]),
        (FakeEventPublisher(), ["user_id"]),
        (FakeEventPublisher(), EVENT_ADDITIONAL_DEFAULT),
        (FakeEventPublisher(), ["user_id"]),
    ],
)
def test_should_check_event_config_constructor(event_publisher, event_additional_info):
    _ = EventConfig(event_publisher, event_additional_info)
