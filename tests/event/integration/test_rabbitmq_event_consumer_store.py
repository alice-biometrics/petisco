from time import sleep

import pytest
from meiga import isSuccess, Result, Error, isFailure

from petisco import Event, EventSubscriber

from petisco.fixtures.testing_decorators import testing_with_rabbitmq
from tests.event.mothers.event_user_created_mother import EventUserCreatedMother
from tests.event.mothers.rabbitmq_event_bus_mother import RabbitMqEventBusMother
from tests.event.mothers.rabbitmq_event_configurer_mother import (
    RabbitMqEventConfigurerMother,
)
from tests.event.mothers.rabbitmq_event_consumer_mother import (
    RabbitMqEventConsumerMother,
)
from tests.event.spies.spy_events import SpyEvents


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_consume_from_store_queue_from_rabbitmq():

    spy = SpyEvents()

    def assert_consumer_event_store(event: Event) -> Result[bool, Error]:
        spy.append(event)
        return isSuccess

    event = EventUserCreatedMother.random()

    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_event(event)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.default()

    consumer.consume_store(assert_consumer_event_store)
    consumer.start()

    sleep(2.0)
    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_count_by_event_id(event.event_id, 1)


@pytest.mark.integration
@testing_with_rabbitmq
@pytest.mark.parametrize(
    "max_retries_allowed,expected_number_event_consumed,simulated_results",
    [
        (1, 2, [isFailure, isSuccess]),
        (2, 3, [isFailure, isFailure, isSuccess]),
        (3, 4, [isFailure, isFailure, isFailure, isSuccess]),
        (4, 5, [isFailure, isFailure, isFailure, isFailure, isSuccess]),
    ],
)
def test_should_publish_consume_and_retry_from_store_queue_from_rabbitmq(
    max_retries_allowed, expected_number_event_consumed, simulated_results
):
    spy = SpyEvents()

    def assert_consumer_event_store(event: Event) -> Result[bool, Error]:
        spy.append(event)
        result = simulated_results.pop(0)
        return result

    event = EventUserCreatedMother.random()

    configurer = RabbitMqEventConfigurerMother.with_ttl_10ms()
    configurer.configure_event(event)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(max_retries_allowed)

    consumer.consume_store(assert_consumer_event_store)
    consumer.start()

    sleep(1.0)

    consumer.stop()

    configurer.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_count_by_event_id(event.event_id, expected_number_event_consumed)


@pytest.mark.integration
@testing_with_rabbitmq
@pytest.mark.parametrize(
    "max_retries_allowed,expected_number_event_consumed,simulated_results",
    [
        (1, 2, [isFailure, isSuccess]),
        (2, 3, [isFailure, isFailure, isSuccess]),
        (3, 4, [isFailure, isFailure, isFailure, isSuccess]),
        (4, 5, [isFailure, isFailure, isFailure, isFailure, isSuccess]),
    ],
)
def test_should_publish_consume_and_retry_from_store_queue_not_affecting_other_queue_from_rabbitmq_when_fail_event_storer_consumer(
    max_retries_allowed, expected_number_event_consumed, simulated_results
):
    spy_consumer_event_store = SpyEvents()
    spy_consumer_handler = SpyEvents()

    def assert_consumer_event_store(event: Event) -> Result[bool, Error]:
        spy_consumer_event_store.append(event)
        result = simulated_results.pop(0)
        return result

    def assert_consumer_handler(event: Event) -> Result[bool, Error]:
        spy_consumer_handler.append(event)
        return isSuccess

    event = EventUserCreatedMother.random()
    subscribers = [EventSubscriber(event, [assert_consumer_handler])]

    configurer = RabbitMqEventConfigurerMother.with_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(max_retries_allowed)
    consumer.consume(subscribers)
    consumer.consume_store(assert_consumer_event_store)

    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy_consumer_event_store.assert_number_unique_events(1)
    spy_consumer_event_store.assert_first_event(event)
    spy_consumer_event_store.assert_count_by_event_id(
        event.event_id, expected_number_event_consumed
    )

    spy_consumer_handler.assert_number_unique_events(1)
    spy_consumer_handler.assert_first_event(event)
    spy_consumer_handler.assert_count_by_event_id(event.event_id, 1)
