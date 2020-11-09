import copy
from time import sleep

import pytest
from meiga import isSuccess, isFailure, Result, Error

from petisco import Event
from petisco.event.shared.domain.event_subscriber import EventSubscriber

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
@pytest.mark.parametrize(
    "max_retries_allowed,expected_number_event_consumed,simulated_results",
    [
        (0, 1, [isFailure]),
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
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(max_retries_allowed)
    consumer.add_subscribers(subscribers)
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
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer_1, assert_consumer_2],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.default()
    consumer.add_subscribers(subscribers)
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
        (0, 1, [isFailure]),
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
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer_1, assert_consumer_2],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(max_retries_allowed)
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.5)

    consumer.stop()
    configurer.clear()

    print(f"num events: {len(spy_consumer_1.events)} - {spy_consumer_1}")
    print(f"num events: {len(spy_consumer_2.events)} - {spy_consumer_2}")

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
        (0, 1, [isFailure]),
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
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer_handler],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(max_retries_allowed)
    consumer.add_subscribers(subscribers)
    consumer.add_handler_on_queue("store", assert_consumer_event_store)

    consumer.start()

    sleep(1.0)

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
def test_should_publish_consume_retry_and_send_to_dead_letter_event_from_rabbitmq_when_fail_consumer():
    max_retries_allowed = 2
    expected_number_event_consumed = 3

    spy = SpyEvents()
    spy_dead_letter = SpyEvents()

    def assert_consumer(event: Event) -> Result[bool, Error]:
        spy.append(event)
        return isFailure

    event = EventUserCreatedMother.random()
    subscriber = EventSubscriber(
        event_name=event.event_name,
        event_version=event.event_version,
        handlers=[assert_consumer],
    )
    subscribers = [subscriber]

    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(max_retries_allowed)
    consumer.add_subscribers(subscribers)

    def dead_letter_consumer(event: Event) -> Result[bool, Error]:
        spy_dead_letter.append(event)
        return isSuccess

    consumer.add_subscriber_on_dead_letter(subscriber, dead_letter_consumer)

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
@pytest.mark.parametrize(
    "max_retries_allowed, expected_number_event_consumed_by_store, expected_number_event_consumed_by_handler_1, expected_number_event_consumed_by_handler_2,simulated_results_store, simulated_results_handler_1, simulated_results_handler_2",
    [
        (1, 2, 1, 1, [isFailure, isSuccess], [isSuccess], [isSuccess]),
        (1, 1, 2, 1, [isSuccess], [isFailure, isSuccess], [isSuccess]),
        (1, 1, 1, 2, [isSuccess], [isSuccess], [isFailure, isSuccess]),
        (1, 2, 2, 1, [isFailure, isSuccess], [isFailure, isSuccess], [isSuccess]),
        (2, 2, 1, 1, [isFailure, isSuccess], [isSuccess], [isSuccess]),
        (2, 1, 2, 1, [isSuccess], [isFailure, isSuccess], [isSuccess]),
        (2, 1, 1, 2, [isSuccess], [isSuccess], [isFailure, isSuccess]),
        (2, 2, 2, 1, [isFailure, isSuccess], [isFailure, isSuccess], [isSuccess]),
        (
            2,
            2,
            2,
            2,
            [isFailure, isSuccess],
            [isFailure, isSuccess],
            [isFailure, isSuccess],
        ),
        (3, 3, 1, 1, [isFailure, isFailure, isSuccess], [isSuccess], [isSuccess]),
        (3, 1, 3, 1, [isSuccess], [isFailure, isFailure, isSuccess], [isSuccess]),
        (3, 1, 1, 3, [isSuccess], [isSuccess], [isFailure, isFailure, isSuccess]),
    ],
)
def test_should_publish_consume_and_retry_event_not_affecting_other_queue_including_store_queue_from_rabbitmq(
    max_retries_allowed,
    expected_number_event_consumed_by_store,
    expected_number_event_consumed_by_handler_1,
    expected_number_event_consumed_by_handler_2,
    simulated_results_store,
    simulated_results_handler_1,
    simulated_results_handler_2,
):

    spy_consumer_event_store = SpyEvents()
    spy_consumer_handler_1 = SpyEvents()
    spy_consumer_handler_2 = SpyEvents()

    def assert_consumer_event_store(event: Event) -> Result[bool, Error]:
        spy_consumer_event_store.append(event)
        result = simulated_results_store.pop(0)
        return result

    def assert_consumer_handler_1(event: Event) -> Result[bool, Error]:
        spy_consumer_handler_1.append(event)
        result = simulated_results_handler_1.pop(0)
        return result

    def assert_consumer_handler_2(event: Event) -> Result[bool, Error]:
        spy_consumer_handler_2.append(event)
        result = simulated_results_handler_2.pop(0)
        return result

    event = EventUserCreatedMother.random()
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer_handler_1, assert_consumer_handler_2],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(max_retries_allowed)
    consumer.add_subscribers(subscribers)
    consumer.add_handler_on_store(assert_consumer_event_store)

    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy_consumer_event_store.assert_number_unique_events(1)
    spy_consumer_event_store.assert_first_event(event)
    spy_consumer_event_store.assert_count_by_event_id(
        event.event_id, expected_number_event_consumed_by_store
    )

    spy_consumer_handler_1.assert_number_unique_events(1)
    spy_consumer_handler_1.assert_first_event(event)
    spy_consumer_handler_1.assert_count_by_event_id(
        event.event_id, expected_number_event_consumed_by_handler_1
    )

    spy_consumer_handler_2.assert_number_unique_events(1)
    spy_consumer_handler_2.assert_first_event(event)
    spy_consumer_handler_2.assert_count_by_event_id(
        event.event_id, expected_number_event_consumed_by_handler_2
    )
