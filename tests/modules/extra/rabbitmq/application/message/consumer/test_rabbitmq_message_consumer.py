import copy
from time import sleep
from unittest.mock import Mock, patch

import pytest
from meiga import BoolResult, isFailure, isSuccess
from pika.exceptions import ConnectionClosedByBroker

from petisco import DomainEvent
from petisco.extra.rabbitmq import RabbitMqConnector
from tests.modules.extra.rabbitmq.mother.domain_event_user_created_mother import (
    DomainEventUserCreatedMother,
)
from tests.modules.extra.rabbitmq.mother.message_subscriber_mother import (
    MessageSubscriberMother,
)
from tests.modules.extra.rabbitmq.mother.rabbitmq_domain_event_bus_mother import (
    RabbitMqDomainEventBusMother,
)
from tests.modules.extra.rabbitmq.mother.rabbitmq_message_configurer_mother import (
    RabbitMqMessageConfigurerMother,
)
from tests.modules.extra.rabbitmq.mother.rabbitmq_message_consumer_mother import (
    RabbitMqMessageConsumerMother,
)
from tests.modules.extra.rabbitmq.utils.spy_messages import SpyMessages
from tests.modules.extra.testing_decorators import testing_with_rabbitmq


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_message_consumer_should_reconnect_when_has_been_closed_by_broker():
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(DomainEventUserCreatedMother.random()),
            handler=lambda a: a,
        )
    ]
    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    valid_channel = RabbitMqConnector().get_channel("valid_channel")

    with patch(
        "pika.adapters.blocking_connection.BlockingChannel.start_consuming",
        side_effect=[ConnectionClosedByBroker(1, ""), valid_channel],
    ):
        consumer = RabbitMqMessageConsumerMother.default()
        consumer.add_subscribers(subscribers)
        consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_message_consumer_should_fail_after_try_to_reconnect_max_allowed_attempts():
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(DomainEventUserCreatedMother.random()),
            handler=lambda a: a,
        )
    ]
    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)
    consumer = RabbitMqMessageConsumerMother.default()
    consumer.add_subscribers(subscribers)

    with pytest.raises(ConnectionError) as exc_info:
        with patch(
            "pika.adapters.blocking_connection.BlockingChannel.start_consuming",
            side_effect=[ConnectionClosedByBroker(1, "")],
        ):
            consumer.connector = Mock(RabbitMqConnector)
            consumer.connector.get_channel.side_effect = [ConnectionError()] * 20
            consumer._start()

        consumer.stop()
        configurer.clear()
    assert "Impossible to reconnect consumer" in str(exc_info.value)


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
def test_rabbitmq_message_consumer_should_publish_consume_and_retry_event_from_rabbitmq_when_fail_consumer(
    max_retries_allowed, expected_number_event_consumed, simulated_results
):
    spy = SpyMessages()

    def assert_consumer(domain_event: DomainEvent) -> BoolResult:
        spy.append(domain_event)
        result = simulated_results.pop(0)
        return result

    domain_event = DomainEventUserCreatedMother.random()

    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer
        )
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    consumer = RabbitMqMessageConsumerMother.with_max_retries(max_retries_allowed)
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_messages(1)
    spy.assert_first_message(domain_event)
    spy.assert_last_message(domain_event)
    spy.assert_count_by_message_id(
        domain_event.message_id, expected_number_event_consumed
    )


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_message_consumer_publish_consume_and_retry_event_with_two_handlers_from_rabbitmq():

    spy_consumer_1 = SpyMessages()
    spy_consumer_2 = SpyMessages()

    def assert_consumer_1(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_1.append(domain_event)
        return isSuccess

    def assert_consumer_2(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_2.append(domain_event)
        return isSuccess

    domain_event = DomainEventUserCreatedMother.random()
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer_1
        ),
        MessageSubscriberMother.other_domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer_2
        ),
    ]

    configurer = RabbitMqMessageConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    consumer = RabbitMqMessageConsumerMother.default()
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy_consumer_1.assert_number_unique_messages(1)
    spy_consumer_1.assert_first_message(domain_event)
    spy_consumer_1.assert_count_by_message_id(domain_event.message_id, 1)

    spy_consumer_2.assert_number_unique_messages(1)
    spy_consumer_2.assert_first_message(domain_event)
    spy_consumer_2.assert_count_by_message_id(domain_event.message_id, 1)


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
def test_rabbitmq_message_consumer_publish_consume_and_retry_event_with_two_handlers_from_rabbitmq_when_fail_consumer(
    max_retries_allowed, expected_number_event_consumed, simulated_results
):

    spy_consumer_1 = SpyMessages()
    spy_consumer_2 = SpyMessages()

    simulated_results_1 = copy.deepcopy(simulated_results)
    simulated_results_2 = copy.deepcopy(simulated_results)

    def assert_consumer_1(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_1.append(domain_event)
        result = simulated_results_1.pop(0)
        return result

    def assert_consumer_2(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_2.append(domain_event)
        result = simulated_results_2.pop(0)
        return result

    domain_event = DomainEventUserCreatedMother.random()
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer_1
        ),
        MessageSubscriberMother.other_domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer_2
        ),
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    consumer = RabbitMqMessageConsumerMother.with_max_retries(max_retries_allowed)
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.5)

    consumer.stop()
    configurer.clear()

    print(f"num events: {len(spy_consumer_1.messages)} - {spy_consumer_1}")
    print(f"num events: {len(spy_consumer_2.messages)} - {spy_consumer_2}")

    spy_consumer_1.assert_number_unique_messages(1)
    spy_consumer_1.assert_first_message(domain_event)
    spy_consumer_1.assert_count_by_message_id(
        domain_event.message_id, expected_number_event_consumed
    )

    spy_consumer_2.assert_number_unique_messages(1)
    spy_consumer_2.assert_first_message(domain_event)
    spy_consumer_2.assert_count_by_message_id(
        domain_event.message_id, expected_number_event_consumed
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
def test_rabbitmq_message_consumer_should_publish_consume_and_retry_event_not_affecting_store_queue_from_rabbitmq_when_fail_handler_consumer(
    max_retries_allowed, expected_number_event_consumed, simulated_results
):

    spy_consumer_event_store = SpyMessages()
    spy_consumer_handler = SpyMessages()

    def assert_consumer_event_store(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_event_store.append(domain_event)
        return isSuccess

    def assert_consumer_handler(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_handler.append(domain_event)
        result = simulated_results.pop(0)
        return result

    domain_event = DomainEventUserCreatedMother.random()
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer_handler
        ),
        MessageSubscriberMother.all_messages_subscriber(
            handler=assert_consumer_event_store
        ),
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    consumer = RabbitMqMessageConsumerMother.with_max_retries(max_retries_allowed)
    consumer.add_subscribers(subscribers)

    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy_consumer_event_store.assert_number_unique_messages(1)
    spy_consumer_event_store.assert_first_message(domain_event)
    spy_consumer_event_store.assert_count_by_message_id(domain_event.message_id, 1)

    spy_consumer_handler.assert_number_unique_messages(1)
    spy_consumer_handler.assert_first_message(domain_event)
    spy_consumer_handler.assert_count_by_message_id(
        domain_event.message_id, expected_number_event_consumed
    )


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_message_consumer_publish_consume_retry_and_send_to_dead_letter_event_from_rabbitmq_when_fail_consumer():
    max_retries_allowed = 2
    expected_number_event_consumed = 3

    spy = SpyMessages()
    spy_dead_letter = SpyMessages()

    def assert_consumer(domain_event: DomainEvent) -> BoolResult:
        spy.append(domain_event)
        return isFailure

    domain_event = DomainEventUserCreatedMother.random()
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer
        )
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    consumer = RabbitMqMessageConsumerMother.with_max_retries(max_retries_allowed)
    consumer.add_subscribers(subscribers)

    def dead_letter_consumer(domain_event: DomainEvent) -> BoolResult:
        spy_dead_letter.append(domain_event)
        return isSuccess

    dead_letter_message_subscriber = MessageSubscriberMother.domain_event_subscriber(
        domain_event_type=type(domain_event), handler=dead_letter_consumer
    )

    consumer.add_subscriber_on_dead_letter(dead_letter_message_subscriber)

    consumer.start()

    sleep(2.5)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_messages(1)
    spy.assert_first_message(domain_event)
    spy.assert_count_by_message_id(
        domain_event.message_id, expected_number_event_consumed
    )

    spy_dead_letter.assert_number_unique_messages(1)
    spy_dead_letter.assert_first_message(domain_event)
    spy_dead_letter.assert_count_by_message_id(domain_event.message_id, 1)


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
def test_rabbitmq_message_consumer_should_publish_consume_and_retry_event_not_affecting_other_queue_including_store_queue_from_rabbitmq(
    max_retries_allowed,
    expected_number_event_consumed_by_store,
    expected_number_event_consumed_by_handler_1,
    expected_number_event_consumed_by_handler_2,
    simulated_results_store,
    simulated_results_handler_1,
    simulated_results_handler_2,
):

    spy_consumer_event_store = SpyMessages()
    spy_consumer_handler_1 = SpyMessages()
    spy_consumer_handler_2 = SpyMessages()

    def assert_consumer_event_store(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_event_store.append(domain_event)
        result = simulated_results_store.pop(0)
        return result

    def assert_consumer_handler_1(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_handler_1.append(domain_event)
        result = simulated_results_handler_1.pop(0)
        return result

    def assert_consumer_handler_2(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_handler_2.append(domain_event)
        result = simulated_results_handler_2.pop(0)
        return result

    domain_event = DomainEventUserCreatedMother.random()
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer_handler_1
        ),
        MessageSubscriberMother.other_domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer_handler_2
        ),
        MessageSubscriberMother.all_messages_subscriber(
            handler=assert_consumer_event_store
        ),
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    consumer = RabbitMqMessageConsumerMother.with_max_retries(max_retries_allowed)
    consumer.add_subscribers(subscribers)

    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy_consumer_event_store.assert_number_unique_messages(1)
    spy_consumer_event_store.assert_first_message(domain_event)
    spy_consumer_event_store.assert_count_by_message_id(
        domain_event.message_id, expected_number_event_consumed_by_store
    )

    spy_consumer_handler_1.assert_number_unique_messages(1)
    spy_consumer_handler_1.assert_first_message(domain_event)
    spy_consumer_handler_1.assert_count_by_message_id(
        domain_event.message_id, expected_number_event_consumed_by_handler_1
    )

    spy_consumer_handler_2.assert_number_unique_messages(1)
    spy_consumer_handler_2.assert_first_message(domain_event)
    spy_consumer_handler_2.assert_count_by_message_id(
        domain_event.message_id, expected_number_event_consumed_by_handler_2
    )
