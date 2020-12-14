from time import sleep

import pytest
from meiga import isSuccess, Result, Error

from petisco import Event, IEventBus
from petisco.event.shared.domain.event_subscriber import EventSubscriber

from petisco.fixtures.testing_decorators import testing_with_rabbitmq
from tests.modules.event.mothers.event_user_created_mother import EventUserCreatedMother
from tests.modules.event.mothers.event_user_updated_mother import EventUserUpdatedMother
from tests.modules.event.mothers.rabbitmq_event_bus_mother import RabbitMqEventBusMother
from tests.modules.event.mothers.rabbitmq_event_configurer_mother import (
    RabbitMqEventConfigurerMother,
)
from tests.modules.event.mothers.rabbitmq_event_consumer_mother import (
    RabbitMqEventConsumerMother,
)
from tests.modules.event.spies.spy_events import SpyEvents


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_event_on_consumer():
    spy = SpyEvents()

    def assert_consumer(event: Event, event_bus: IEventBus) -> Result[bool, Error]:
        spy.append(event)
        event = EventUserUpdatedMother.random()
        event_bus.publish(event)
        return isSuccess

    event = EventUserCreatedMother.random()
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    consumer = RabbitMqEventConsumerMother.with_max_retries(1)
    consumer.add_subscribers(subscribers)
    consumer.start()

    bus = RabbitMqEventBusMother.default()
    for _ in range(5):
        event = EventUserCreatedMother.random()
        bus.publish(event)

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(5)
