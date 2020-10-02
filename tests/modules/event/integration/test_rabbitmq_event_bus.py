import pytest

from petisco.fixtures.testing_decorators import testing_with_rabbitmq
from tests.modules.event.mothers.event_user_created_mother import EventUserCreatedMother
from tests.modules.event.mothers.rabbitmq_event_bus_mother import RabbitMqEventBusMother
from tests.modules.event.mothers.rabbitmq_event_configurer_mother import (
    RabbitMqEventConfigurerMother,
)


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_event_without_rabbitmq_configuration():
    event = EventUserCreatedMother.random()

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    bus.configurer.clear()


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_event_with_previous_rabbitmq_configuration():
    event = EventUserCreatedMother.random()

    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_event(event)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    configurer.clear()
