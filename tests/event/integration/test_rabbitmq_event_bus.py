import copy
from time import sleep

import pytest
from meiga import isSuccess, isFailure, Result, Error

from petisco import RabbitMqConnector, Event
from petisco.event.shared.domain.event_subscriber import EventSubscriber

from petisco.fixtures.testing_decorators import testing_with_rabbitmq
from tests.event.mothers.defaults import DEFAULT_EXCHANGE_NAME
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
@pytest.mark.parametrize(
    "max_retries_allowed,expected_number_event_consumed,simulated_results",
    [
        (1, 2, [isFailure, isSuccess]),
        (2, 3, [isFailure, isFailure, isSuccess]),
        (3, 4, [isFailure, isFailure, isFailure, isSuccess]),
        (4, 5, [isFailure, isFailure, isFailure, isFailure, isSuccess]),
    ],
)
def test_should_publish_consume_and_retry_event_from_rabbitmq_when_fail_consumer(
    max_retries_allowed, expected_number_event_consumed, simulated_results
):
    spy = SpyEvents()

    def assert_consumer(event: Event) -> Result[bool, Error]:
        spy.append(event)
        result = simulated_results.pop(0)
        return result

    event = EventUserCreatedMother.random()
    subscribers = [EventSubscriber(event, [assert_consumer])]

    configurer = RabbitMqEventConfigurerMother.with_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(max_retries_allowed)
    consumer.consume(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_last_event(event)
    spy.assert_count_by_event_id(event.event_id, expected_number_event_consumed)


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_consume_and_retry_event_with_two_handlers_from_rabbitmq():

    spy_consumer_1 = SpyEvents()
    spy_consumer_2 = SpyEvents()

    def assert_consumer_1(event: Event) -> Result[bool, Error]:
        spy_consumer_1.append(event)
        return isSuccess

    def assert_consumer_2(event: Event) -> Result[bool, Error]:
        spy_consumer_2.append(event)
        return isSuccess

    event = EventUserCreatedMother.random()
    subscribers = [EventSubscriber(event, [assert_consumer_1, assert_consumer_2])]

    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.default()
    consumer.consume(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy_consumer_1.assert_number_unique_events(1)
    spy_consumer_1.assert_first_event(event)
    spy_consumer_1.assert_count_by_event_id(event.event_id, 1)

    spy_consumer_2.assert_number_unique_events(1)
    spy_consumer_2.assert_first_event(event)
    spy_consumer_2.assert_count_by_event_id(event.event_id, 1)


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
def test_should_publish_consume_and_retry_event_with_two_handlers_from_rabbitmq_when_fail_consumer(
    max_retries_allowed, expected_number_event_consumed, simulated_results
):

    spy_consumer_1 = SpyEvents()
    spy_consumer_2 = SpyEvents()

    simulated_results_1 = copy.deepcopy(simulated_results)
    simulated_results_2 = copy.deepcopy(simulated_results)

    def assert_consumer_1(event: Event) -> Result[bool, Error]:
        spy_consumer_1.append(event)
        result = simulated_results_1.pop(0)
        return result

    def assert_consumer_2(event: Event) -> Result[bool, Error]:
        spy_consumer_2.append(event)
        result = simulated_results_2.pop(0)
        return result

    event = EventUserCreatedMother.random()
    subscribers = [EventSubscriber(event, [assert_consumer_1, assert_consumer_2])]

    configurer = RabbitMqEventConfigurerMother.with_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(max_retries_allowed)
    consumer.consume(subscribers)
    consumer.start()

    sleep(2.0)

    consumer.stop()
    configurer.clear()

    spy_consumer_1.assert_number_unique_events(1)
    spy_consumer_1.assert_first_event(event)
    spy_consumer_1.assert_count_by_event_id(
        event.event_id, expected_number_event_consumed
    )

    spy_consumer_2.assert_number_unique_events(1)
    spy_consumer_2.assert_first_event(event)
    spy_consumer_2.assert_count_by_event_id(
        event.event_id, expected_number_event_consumed
    )


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
def test_should_publish_consume_and_retry_event_not_affecting_store_queue_from_rabbitmq_when_fail_handler_consumer(
    max_retries_allowed, expected_number_event_consumed, simulated_results
):

    spy_consumer_event_store = SpyEvents()
    spy_consumer_handler = SpyEvents()

    def assert_consumer_event_store(event: Event) -> Result[bool, Error]:
        spy_consumer_event_store.append(event)
        return isSuccess

    def assert_consumer_handler(event: Event) -> Result[bool, Error]:
        spy_consumer_handler.append(event)
        result = simulated_results.pop(0)
        return result

    event = EventUserCreatedMother.random()
    subscribers = [EventSubscriber(event, [assert_consumer_handler])]

    configurer = RabbitMqEventConfigurerMother.with_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(max_retries_allowed)
    consumer.consume(subscribers)
    consumer.consume_queue("store", assert_consumer_event_store)

    consumer.start()

    sleep(2.0)

    consumer.stop()
    configurer.clear()

    spy_consumer_event_store.assert_number_unique_events(1)
    spy_consumer_event_store.assert_first_event(event)
    spy_consumer_event_store.assert_count_by_event_id(event.event_id, 1)

    spy_consumer_handler.assert_number_unique_events(1)
    spy_consumer_handler.assert_first_event(event)
    spy_consumer_handler.assert_count_by_event_id(
        event.event_id, expected_number_event_consumed
    )


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_consume_only_from_store_queue_from_rabbitmq():

    spy = SpyEvents()

    def assert_consumer_event_store(event: Event) -> Result[bool, Error]:
        print(f"assert_consumer_event_store on {event}")
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
def test_should_publish_consume_retry_and_send_to_dead_letter_event_from_rabbitmq_when_fail_consumer():
    max_retries_allowed = 1
    expected_number_event_consumed = 2

    spy = SpyEvents()
    spy_dead_letter = SpyEvents()

    def assert_consumer(event: Event) -> Result[bool, Error]:
        spy.append(event)
        return isFailure

    event = EventUserCreatedMother.random()
    subscriber = EventSubscriber(event, [assert_consumer])
    subscribers = [subscriber]

    configurer = RabbitMqEventConfigurerMother.with_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(max_retries_allowed)
    consumer.consume(subscribers)

    def dead_letter_consumer(event: Event) -> Result[bool, Error]:
        spy_dead_letter.append(event)
        return isSuccess

    consumer.consume_dead_letter(subscriber, dead_letter_consumer)

    consumer.start()

    sleep(1.5)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_count_by_event_id(event.event_id, expected_number_event_consumed)

    spy_dead_letter.assert_number_unique_events(1)
    spy_dead_letter.assert_first_event(event)
    spy_dead_letter.assert_count_by_event_id(event.event_id, 1)


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_recover_from_connection_error_when_publish_an_event(
    make_user_created_event,
):
    connector = RabbitMqConnector()
    original_wait_seconds_retry = connector.wait_seconds_retry
    connector.wait_seconds_retry = 0.1

    configurer = RabbitMqEventConfigurerMother.default(connector)

    event = make_user_created_event()

    configurer.configure_event(event)

    bus = RabbitMqEventBusMother.default(connector)

    connection = connector.get_connection(DEFAULT_EXCHANGE_NAME)

    connection.close()

    bus.publish(event)

    connector.wait_seconds_retry = original_wait_seconds_retry

    configurer.clear()
