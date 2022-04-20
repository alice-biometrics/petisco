from time import sleep

import pytest
from meiga import BoolResult, isSuccess

from petisco import DomainEvent
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


class DomainEvent1(DomainEvent):
    pass


class DomainEvent2(DomainEvent):
    pass


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_should_configure_queues_to_resist_the_absence_of_consumers():
    spy_consumer_1 = SpyMessages()
    spy_consumer_2 = SpyMessages()
    spy_dead_letter_1 = SpyMessages()
    spy_dead_letter_2 = SpyMessages()

    def assert_consumer_1(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_1.append(domain_event)
        return isSuccess

    def assert_consumer_2(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_2.append(domain_event)
        return isSuccess

    def assert_dead_letter_1(domain_event: DomainEvent) -> BoolResult:
        spy_dead_letter_1.append(domain_event)
        return isSuccess

    def assert_dead_letter_2(domain_event: DomainEvent) -> BoolResult:
        spy_dead_letter_2.append(domain_event)
        return isSuccess

    domain_event_1 = DomainEvent1()
    domain_event_2 = DomainEvent2()

    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event_1), handler=assert_consumer_1
        ),
        MessageSubscriberMother.other_domain_event_subscriber(
            domain_event_type=type(domain_event_2), handler=assert_consumer_2
        ),
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event_1)
    bus.publish(domain_event_2)

    sleep(2.0)

    consumer = RabbitMqMessageConsumerMother.default()
    consumer.add_subscriber_on_dead_letter(
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event_1), handler=assert_dead_letter_1
        )
    )
    consumer.add_subscriber_on_dead_letter(
        MessageSubscriberMother.other_domain_event_subscriber(
            domain_event_type=type(domain_event_2), handler=assert_dead_letter_2
        )
    )
    consumer.start()

    sleep(3.0)

    consumer.stop()
    configurer.clear()

    spy_consumer_1.assert_number_unique_messages(0)
    spy_consumer_2.assert_number_unique_messages(0)

    spy_dead_letter_1.assert_number_unique_messages(1)
    spy_dead_letter_1.assert_first_message(domain_event_1)
    spy_dead_letter_1.assert_count_by_message_id(domain_event_1.message_id, 1)

    spy_dead_letter_2.assert_number_unique_messages(1)
    spy_dead_letter_2.assert_first_message(domain_event_2)
    spy_dead_letter_2.assert_count_by_message_id(domain_event_2.message_id, 1)
