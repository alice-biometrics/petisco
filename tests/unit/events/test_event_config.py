import pytest

from petisco import EventConfig
from petisco.events.event_config import (
    EVENT_MANAGER_DEFAULT,
    EVENT_TOPIC_DEFAULT,
    EVENT_ADDITIONAL_DEFAULT,
)
from tests.unit.mocks.fake_event_manager import FakeEventManager


@pytest.mark.unit
def test_should_check_default_event_config_is_non_configured():

    event_config = EventConfig()

    assert not event_config.is_configured


@pytest.mark.unit
@pytest.mark.parametrize(
    "event_manager,event_topic,event_additional_info",
    [
        (FakeEventManager(), EVENT_TOPIC_DEFAULT, EVENT_ADDITIONAL_DEFAULT),
        (EVENT_MANAGER_DEFAULT, "my-event-topic", EVENT_ADDITIONAL_DEFAULT),
        (EVENT_MANAGER_DEFAULT, EVENT_TOPIC_DEFAULT, ["user_id"]),
        (EVENT_MANAGER_DEFAULT, "my-event-topic", ["user_id"]),
        (FakeEventManager(), EVENT_TOPIC_DEFAULT, ["user_id"]),
        (FakeEventManager(), "my-event-topic", EVENT_ADDITIONAL_DEFAULT),
        (FakeEventManager(), "my-event-topic", ["user_id"]),
    ],
)
def test_should_check_event_config_is_configured(
    event_manager, event_topic, event_additional_info
):

    event_config = EventConfig(event_manager, event_topic, event_additional_info)

    assert event_config.is_configured
