import pytest
import os

from petisco import Petisco
from petisco.event.bus.infrastructure.not_implemented_event_bus import (
    NotImplementedEventBus,
)
from petisco.event.bus.infrastructure.rabbitmq_event_bus import RabbitMqEventBus
from petisco.fixtures.testing_decorators import testing_with_rabbitmq


@pytest.mark.end2end
def test_should_load_petisco_from_yml_and_configure_events_from_yml_with_not_implemented_message_broker(
    petisco_yml_path_end2end,
):
    Petisco.clear()

    filename = f"{petisco_yml_path_end2end}/petisco.all.yml"
    filename_events = f"{petisco_yml_path_end2end}/petisco.events.not_implemented.yml"

    petisco = Petisco.from_filename(filename)
    petisco.configure_events(filename_events)

    petisco._start()

    assert isinstance(Petisco.get_event_bus(), NotImplementedEventBus)

    petisco.stop()
    Petisco.clear()


@pytest.mark.end2end
@testing_with_rabbitmq
def test_should_load_petisco_from_yml_and_configure_events_from_yml_with_rabbitmq_message_broker(
    petisco_yml_path_end2end,
):
    Petisco.clear()

    filename = f"{petisco_yml_path_end2end}/petisco.all.yml"
    filename_events = f"{petisco_yml_path_end2end}/petisco.events.yml"

    petisco = Petisco.from_filename(filename)
    petisco.configure_events(filename_events)
    petisco._start()
    assert isinstance(Petisco.get_event_bus(), RabbitMqEventBus)

    assert "config_events" in petisco.info

    petisco.stop()
    Petisco.clear()


@pytest.mark.end2end
@testing_with_rabbitmq
def test_should_load_petisco_from_yml_and_configure_events_from_yml_with_not_implemented_message_broker_but_configured_with_environ(
    petisco_yml_path_end2end,
):
    Petisco.clear()

    filename = f"{petisco_yml_path_end2end}/petisco.all.yml"
    filename_events = f"{petisco_yml_path_end2end}/petisco.events.not_implemented.yml"
    os.environ["PETISCO_EVENT_MESSAGE_BROKER"] = "rabbitmq"

    petisco = Petisco.from_filename(filename)
    petisco.configure_events(filename_events)

    petisco._start()

    assert isinstance(Petisco.get_event_bus(), RabbitMqEventBus)

    del os.environ["PETISCO_EVENT_MESSAGE_BROKER"]

    petisco.stop()

    Petisco.clear()


@pytest.mark.end2end
@testing_with_rabbitmq
def test_should_load_petisco_from_yml_and_configure_events_from_yml_with_environ_rabbitmq_message_broker_not_implemented(
    petisco_yml_path_end2end,
):
    Petisco.clear()
    os.environ["PETISCO_EVENT_MESSAGE_BROKER"] = "notimplemented"

    filename = f"{petisco_yml_path_end2end}/petisco.all.yml"
    filename_events = f"{petisco_yml_path_end2end}/petisco.events.yml"

    petisco = Petisco.from_filename(filename)
    petisco.configure_events(filename_events)
    petisco._start()
    assert isinstance(Petisco.get_event_bus(), NotImplementedEventBus)

    del os.environ["PETISCO_EVENT_MESSAGE_BROKER"]

    petisco.stop()
    Petisco.clear()


@pytest.mark.end2end
def test_should_load_petisco_from_yml_with_specific_queue_config(
    petisco_yml_path_end2end,
):
    Petisco.clear()

    filename = f"{petisco_yml_path_end2end}/petisco.all.yml"
    filename_events = f"{petisco_yml_path_end2end}/petisco.events.specific.yml"

    petisco = Petisco.from_filename(filename)
    petisco.configure_events(filename_events)
    petisco._start()

    assert "config_events" in petisco.info
    assert "queues_specific_config" in petisco.info.get("config_events")

    petisco.stop()
    Petisco.clear()
