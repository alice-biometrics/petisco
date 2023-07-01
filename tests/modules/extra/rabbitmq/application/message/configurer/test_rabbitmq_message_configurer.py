from time import sleep
from typing import Callable, List

import pytest
from meiga import BoolResult, isSuccess

from petisco import DomainEvent, DomainEventSubscriber
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
class TestRabbitMqMessageConfigurer:
    spy_consumer_1: SpyMessages
    spy_consumer_2: SpyMessages
    spy_dead_letter_1: SpyMessages
    spy_dead_letter_2: SpyMessages
    domain_event_1: DomainEvent1
    domain_event_2: DomainEvent2
    subscribers: List[DomainEventSubscriber]
    assert_dead_letter_1: Callable
    assert_dead_letter_2: Callable

    def setup_method(self):
        self.spy_consumer_1 = SpyMessages()
        self.spy_consumer_2 = SpyMessages()
        self.spy_dead_letter_1 = SpyMessages()
        self.spy_dead_letter_2 = SpyMessages()

        def _assert_consumer_1(domain_event: DomainEvent) -> BoolResult:
            self.spy_consumer_1.append(domain_event)
            return isSuccess

        def _assert_consumer_2(domain_event: DomainEvent) -> BoolResult:
            self.spy_consumer_2.append(domain_event)
            return isSuccess

        def _assert_dead_letter_1(domain_event: DomainEvent) -> BoolResult:
            self.spy_dead_letter_1.append(domain_event)
            return isSuccess

        def _assert_dead_letter_2(domain_event: DomainEvent) -> BoolResult:
            self.spy_dead_letter_2.append(domain_event)
            return isSuccess

        self.domain_event_1 = DomainEvent1()
        self.domain_event_2 = DomainEvent2()

        self.subscribers = [
            MessageSubscriberMother.domain_event_subscriber(
                domain_event_type=type(self.domain_event_1), handler=_assert_consumer_1
            ),
            MessageSubscriberMother.other_domain_event_subscriber(
                domain_event_type=type(self.domain_event_2), handler=_assert_consumer_2
            ),
        ]

        self.assert_dead_letter_1 = _assert_dead_letter_1
        self.assert_dead_letter_2 = _assert_dead_letter_2

    @testing_with_rabbitmq
    def should_configure_queues_to_resist_the_absence_of_consumers(self):
        configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
        configurer.configure_subscribers(self.subscribers)

        bus = RabbitMqDomainEventBusMother.default()
        bus.publish(self.domain_event_1)
        bus.publish(self.domain_event_2)

        sleep(2.0)

        consumer = RabbitMqMessageConsumerMother.default()
        consumer.add_subscriber_on_dead_letter(
            MessageSubscriberMother.domain_event_subscriber(
                domain_event_type=type(self.domain_event_1),
                handler=self.assert_dead_letter_1,
            )
        )
        consumer.add_subscriber_on_dead_letter(
            MessageSubscriberMother.other_domain_event_subscriber(
                domain_event_type=type(self.domain_event_2),
                handler=self.assert_dead_letter_2,
            )
        )
        consumer.start()

        sleep(3.0)

        consumer.stop()
        configurer.clear()

        self.spy_consumer_1.assert_number_unique_messages(0)
        self.spy_consumer_2.assert_number_unique_messages(0)

        self.spy_dead_letter_1.assert_number_unique_messages(1)
        self.spy_dead_letter_1.assert_first_message(self.domain_event_1)
        self.spy_dead_letter_1.assert_count_by_message_id(
            self.domain_event_1.get_message_id(), 1
        )

        self.spy_dead_letter_2.assert_number_unique_messages(1)
        self.spy_dead_letter_2.assert_first_message(self.domain_event_2)
        self.spy_dead_letter_2.assert_count_by_message_id(
            self.domain_event_2.get_message_id(), 1
        )

    @testing_with_rabbitmq
    def should_configure_queues_with_clear_before(self):
        configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
        configurer.configure_subscribers(self.subscribers)

        configurer.configure_subscribers(
            self.subscribers, clear_subscriber_before=True, clear_store_before=True
        )

        configurer.clear()
