from time import sleep

import pytest
from meiga import isSuccess, BoolResult

from petisco import Event

from petisco.fixtures.testing_decorators import testing_with_rabbitmq
from tests.modules.event.mothers.event_user_created_mother import EventUserCreatedMother
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
def test_should_publish_consume_from_store_queue_from_rabbitmq_with_stop_and_start():

    spy = SpyEvents()

    def assert_consumer_event_store(event: Event) -> BoolResult:
        spy.append(event)
        return isSuccess

    bus = RabbitMqEventBusMother.default()

    first_event = EventUserCreatedMother.random()
    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_event(first_event)

    # First Start & Stop
    bus.publish(first_event)
    first_consumer = RabbitMqEventConsumerMother.default()
    first_consumer.add_handler_on_store(assert_consumer_event_store)
    first_consumer.start()
    sleep(1.0)
    first_consumer.stop()

    # Second Start & Stop
    second_event = EventUserCreatedMother.random()
    second_consumer = RabbitMqEventConsumerMother.default()
    second_consumer.add_handler_on_store(assert_consumer_event_store)
    second_consumer.start()
    bus.publish(second_event)
    sleep(1.0)
    second_consumer.stop()

    configurer.clear()

    spy.assert_number_unique_events(2)
    spy.assert_count_by_event_id(first_event.event_id, 1)
    spy.assert_count_by_event_id(second_event.event_id, 1)
