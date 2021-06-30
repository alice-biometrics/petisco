from time import sleep

import pytest
from meiga import isSuccess, BoolResult, isFailure

from petisco import DomainEvent

from petisco.legacy.fixtures.testing_decorators import testing_with_rabbitmq
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


@pytest.mark.integration
@testing_with_rabbitmq
def test_message_consumer_should_publish_consume_from_store_queue_from_rabbitmq_with_stop_and_start():

    spy = SpyMessages()

    def assert_consumer_event_store(domain_event: DomainEvent) -> BoolResult:
        spy.append(domain_event)
        return isSuccess

    bus = RabbitMqDomainEventBusMother.default()
    subscribers = [
        MessageSubscriberMother.all_messages_subscriber(
            handler=assert_consumer_event_store
        )
    ]

    configurer = RabbitMqMessageConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    # First Start & Stop
    first_consumer = RabbitMqMessageConsumerMother.default()
    first_consumer.add_subscribers(subscribers)
    first_consumer.start()
    first_event = DomainEventUserCreatedMother.random()
    bus.publish(first_event)
    sleep(1.0)
    first_consumer.stop()

    # Second Start & Stop
    second_consumer = RabbitMqMessageConsumerMother.default()
    second_consumer.add_subscribers(subscribers)
    second_consumer.start()
    second_event = DomainEventUserCreatedMother.random()
    bus.publish(second_event)
    sleep(1.0)
    second_consumer.stop()

    configurer.clear()

    spy.assert_number_unique_messages(2)
    spy.assert_count_by_message_id(first_event.message_id, 1)
    spy.assert_count_by_message_id(second_event.message_id, 1)


@pytest.mark.integration
@testing_with_rabbitmq
def test_message_consumer_should_unsubscribe_and_resume_handler_on_store_queue():

    spy = SpyMessages()
    spy_dead_letter = SpyMessages()

    def assert_consumer_event_store(domain_event: DomainEvent) -> BoolResult:
        spy.append(domain_event)
        return isSuccess

    def assert_consumer_event_dead_letter(domain_event: DomainEvent) -> BoolResult:
        spy_dead_letter.append(domain_event)
        return isSuccess

    bus = RabbitMqDomainEventBusMother.default()

    subscribers = [
        MessageSubscriberMother.all_messages_subscriber(
            handler=assert_consumer_event_store
        )
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    # Consumer configuration
    consumer = RabbitMqMessageConsumerMother.default()
    consumer.add_subscribers(subscribers)
    consumer.add_subscriber_on_queue(
        queue_name="dead_letter.store",
        subscriber=MessageSubscriberMother.all_messages_subscriber(
            handler=assert_consumer_event_dead_letter
        ),
    )
    consumer.start()

    # Send First Domain Event
    first_event = DomainEventUserCreatedMother.random()
    bus.publish(first_event)
    sleep(1.0)

    # Unsubscribe store Queue
    consumer.unsubscribe_subscriber_on_queue("store")

    # Send 5 Domain Events (Expected to go to dead_letter.store Queue)
    for i in range(5):
        bus.publish(DomainEventUserCreatedMother.random())
    sleep(5.0)

    # Resume Consumer on store Queue
    consumer.resume_subscriber_on_queue("store")

    # Send Second Domain Event
    second_event = DomainEventUserCreatedMother.random()
    bus.publish(second_event)
    sleep(3.0)
    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_messages(2)
    spy.assert_count_by_message_id(first_event.message_id, 1)
    spy.assert_count_by_message_id(second_event.message_id, 1)
    spy_dead_letter.assert_number_unique_messages(5)


@pytest.mark.integration
@testing_with_rabbitmq
def test_message_consumer_should_unsubscribe_and_resume_handler_on_dead_letter_store_queue():

    spy_dead_letter = SpyMessages()

    def assert_consumer_event_store(domain_event: DomainEvent) -> BoolResult:
        return isFailure

    def assert_consumer_event_dead_letter(domain_event: DomainEvent) -> BoolResult:
        spy_dead_letter.append(domain_event)
        return isSuccess

    bus = RabbitMqDomainEventBusMother.default()

    subscribers = [
        MessageSubscriberMother.all_messages_subscriber(
            handler=assert_consumer_event_store
        )
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    # Consumer configuration
    consumer = RabbitMqMessageConsumerMother.default()
    consumer.add_subscribers(subscribers)
    consumer.add_subscriber_on_queue(
        queue_name="dead_letter.store",
        subscriber=MessageSubscriberMother.all_messages_subscriber(
            handler=assert_consumer_event_dead_letter
        ),
    )
    consumer.start()

    for i in range(5):
        bus.publish(DomainEventUserCreatedMother.random())
    sleep(5.0)

    consumer.unsubscribe_subscriber_on_queue("dead_letter.store")

    for i in range(5):
        bus.publish(DomainEventUserCreatedMother.random())
    sleep(5.0)

    consumer.resume_subscriber_on_queue("dead_letter.store")

    for i in range(5):
        bus.publish(DomainEventUserCreatedMother.random())
    sleep(5.0)

    consumer.stop()
    configurer.clear()

    spy_dead_letter.assert_number_unique_messages(15)


@pytest.mark.integration
@testing_with_rabbitmq
def test_message_consumer_should_raise_an_error_when_unsubscribe_an_nonexistent_queue():
    def assert_consumer_event_store(domain_event: DomainEvent) -> BoolResult:
        return isSuccess

    subscribers = [
        MessageSubscriberMother.all_messages_subscriber(
            handler=assert_consumer_event_store
        )
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    # Consumer configuration
    consumer = RabbitMqMessageConsumerMother.default()
    consumer.add_subscribers(subscribers)
    consumer.start()

    with pytest.raises(IndexError) as excinfo:
        consumer.unsubscribe_subscriber_on_queue("nonexistent_queue")
        assert (
            "Cannot unsubscribe an nonexistent queue (nonexistent_queue). Please, check configured consumers"
            in str(excinfo.value)
        )

    consumer.stop()
    configurer.clear()


@pytest.mark.integration
@testing_with_rabbitmq
def test_message_consumer_should_raise_an_error_when_resume_an_nonexistent_queue():
    def assert_consumer_event_store(domain_event: DomainEvent) -> BoolResult:
        return isSuccess

    subscribers = [
        MessageSubscriberMother.all_messages_subscriber(
            handler=assert_consumer_event_store
        )
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    # Consumer configuration
    consumer = RabbitMqMessageConsumerMother.default()
    consumer.add_subscribers(subscribers)
    consumer.start()

    with pytest.raises(IndexError) as excinfo:
        consumer.resume_subscriber_on_queue("nonexistent_queue")
        assert (
            "Cannot resume an nonexistent queue (nonexistent_queue). Please, check configured consumers"
            in str(excinfo.value)
        )
    consumer.stop()
    configurer.clear()
