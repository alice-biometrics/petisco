from time import sleep

import pytest
from meiga import BoolResult, isSuccess

from petisco import DomainEvent
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
def test_rabbitmq_domain_event_bus_should_publish_event_without_rabbitmq_configuration():
    domain_event = DomainEventUserCreatedMother.random()

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    bus.configurer.clear()


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_domain_event_bus_should_publish_event_without_rabbitmq_configuration_and_info_id():
    domain_event = DomainEventUserCreatedMother.random()

    bus = RabbitMqDomainEventBusMother.with_info_id()
    bus.publish(domain_event)
    bus.configurer.clear()


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_domain_event_bus_should_publish_event_with_previous_rabbitmq_configuration():
    domain_event = DomainEventUserCreatedMother.random()

    configurer = RabbitMqMessageConfigurerMother.default()
    configurer.configure()

    bus = RabbitMqDomainEventBusMother.with_info_id()
    bus.publish(domain_event)

    configurer.clear()


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_domain_event_bus_should_publish_event_only_on_store_queue_with_previous_rabbitmq_configuration():
    domain_event = DomainEventUserCreatedMother.random()

    configurer = RabbitMqMessageConfigurerMother.default()
    configurer.configure()

    bus = RabbitMqDomainEventBusMother.with_info_id()
    bus.retry_publish_only_on_store_queue(domain_event)

    configurer.clear()


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_domain_event_bus_should_retry_publish_only_on_store_queue_not_affecting_default_event_queue():

    spy_consumer_default_queue = SpyMessages()
    spy_consumer_store = SpyMessages()

    def assert_consumer_default_queue(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_default_queue.append(domain_event)
        return isSuccess

    def assert_consumer_store(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_store.append(domain_event)
        return isSuccess

    domain_event = DomainEventUserCreatedMother.random()

    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer_default_queue
        ),
        MessageSubscriberMother.all_messages_subscriber(handler=assert_consumer_store),
    ]

    configurer = RabbitMqMessageConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.with_info_id()
    bus.retry_publish_only_on_store_queue(domain_event)

    consumer = RabbitMqMessageConsumerMother.default()
    consumer.add_subscribers(subscribers)

    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy_consumer_default_queue.assert_number_unique_messages(0)
    spy_consumer_default_queue.assert_count_by_message_id(domain_event.message_id, 0)
    spy_consumer_store.assert_number_unique_messages(1)
    spy_consumer_store.assert_first_message(domain_event)
    spy_consumer_store.assert_count_by_message_id(domain_event.message_id, 1)


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_domain_event_bus_should_publish_and_then_consumer_retry_publish_only_on_store_queue_not_affecting_default_event_queue():

    spy_consumer_default_queue = SpyMessages()
    spy_consumer_store = SpyMessages()

    def assert_consumer_default_queue(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_default_queue.append(domain_event)
        bus = RabbitMqDomainEventBusMother.default()
        bus.retry_publish_only_on_store_queue(domain_event)
        return isSuccess

    def assert_consumer_store(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_store.append(domain_event)
        return isSuccess

    domain_event = DomainEventUserCreatedMother.random()

    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer_default_queue
        ),
        MessageSubscriberMother.all_messages_subscriber(handler=assert_consumer_store),
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

    spy_consumer_default_queue.assert_count_by_message_id(domain_event.message_id, 1)
    spy_consumer_store.assert_count_by_message_id(domain_event.message_id, 2)
