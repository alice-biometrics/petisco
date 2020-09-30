import pytest
import os

from petisco import Petisco
from petisco.event.bus.infrastructure.not_implemented_event_bus import (
    NotImplementedEventBus,
)
from petisco.event.bus.infrastructure.rabbitmq_event_bus import RabbitMqEventBus
from petisco.fixtures.testing_decorators import testing_with_rabbitmq


@pytest.fixture
def petisco_yml_path():
    return f"{os.path.dirname(os.path.abspath(__file__))}"


@pytest.mark.unit
def test_should_load_petisco_from_yml_and_configure_events_from_yml_with_not_implemented_message_broker(
    petisco_yml_path
):

    filename = f"{petisco_yml_path}/ymls/petisco.all.yml"
    filename_events = f"{petisco_yml_path}/ymls/petisco.events.not_implemented.yml"

    petisco = Petisco.from_filename(filename)
    petisco.configure_events(filename_events)

    petisco.stop_consuming_events()

    assert isinstance(Petisco.get_event_bus(), NotImplementedEventBus)

    Petisco.clear()


@pytest.mark.unit
@testing_with_rabbitmq
def test_should_load_petisco_from_yml_and_configure_events_from_yml_with_rabbitmq_message_broker(
    petisco_yml_path
):

    filename = f"{petisco_yml_path}/ymls/petisco.all.yml"
    filename_events = f"{petisco_yml_path}/ymls/petisco.events.yml"

    petisco = Petisco.from_filename(filename)
    petisco.configure_events(filename_events)
    petisco.stop_consuming_events()

    assert isinstance(Petisco.get_event_bus(), RabbitMqEventBus)

    Petisco.clear()
