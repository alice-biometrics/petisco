from time import sleep

import pytest
from meiga import BoolResult, isSuccess

from petisco import Event, EventSubscriber
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


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_event_only_on_store_queue_with_previous_rabbitmq_configuration():
    event = EventUserCreatedMother.random()

    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_event(event)

    bus = RabbitMqEventBusMother.default()
    bus.retry_publish_only_on_store_queue(event)

    configurer.clear()


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_retry_publish_only_on_store_queue_not_affecting_default_event_queue():

    spy_consumer_default_queue = SpyEvents()
    spy_consumer_store = SpyEvents()

    def assert_consumer_default_queue(event: Event) -> BoolResult:
        spy_consumer_default_queue.append(event)
        return isSuccess

    def assert_consumer_store(event: Event) -> BoolResult:
        spy_consumer_store.append(event)
        return isSuccess

    event = EventUserCreatedMother.random()
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer_default_queue],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.retry_publish_only_on_store_queue(event)

    consumer = RabbitMqEventConsumerMother.default()
    consumer.add_subscribers(subscribers)
    consumer.add_handler_on_store(assert_consumer_store)

    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy_consumer_default_queue.assert_number_unique_events(0)
    spy_consumer_default_queue.assert_count_by_event_id(event.event_id, 0)
    spy_consumer_store.assert_number_unique_events(1)
    spy_consumer_store.assert_first_event(event)
    spy_consumer_store.assert_count_by_event_id(event.event_id, 1)


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_and_then_consumer_retry_publish_only_on_store_queue_not_affecting_default_event_queue():

    spy_consumer_default_queue = SpyEvents()
    spy_consumer_store = SpyEvents()

    def assert_consumer_default_queue(event: Event) -> BoolResult:
        spy_consumer_default_queue.append(event)
        bus = RabbitMqEventBusMother.default()
        bus.retry_publish_only_on_store_queue(event)
        return isSuccess

    def assert_consumer_store(event: Event) -> BoolResult:
        spy_consumer_store.append(event)
        return isSuccess

    event = EventUserCreatedMother.random()
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer_default_queue],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.default()
    consumer.add_subscribers(subscribers)
    consumer.add_handler_on_store(assert_consumer_store)

    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy_consumer_default_queue.assert_count_by_event_id(event.event_id, 1)
    spy_consumer_store.assert_count_by_event_id(event.event_id, 2)
