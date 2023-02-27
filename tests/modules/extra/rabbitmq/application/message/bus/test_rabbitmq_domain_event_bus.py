from time import sleep
from unittest import mock
from unittest.mock import Mock, patch

import pytest
from meiga import BoolResult, isSuccess
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import ChannelClosedByBroker

from petisco import DomainEvent, DomainEventBus
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
class TestRabbitMqDomainEventBus:
    domain_event: DomainEvent

    def setup_method(self):
        self.domain_event = DomainEventUserCreatedMother.random()

    @testing_with_rabbitmq
    def should_publish_domain_event_without_rabbitmq_configuration(self):
        bus = RabbitMqDomainEventBusMother.default()
        bus.publish(self.domain_event)

        bus.configurer.clear()

    @testing_with_rabbitmq
    def should_publish_domain_event_without_rabbitmq_configuration_and_info_id(self):
        bus = RabbitMqDomainEventBusMother.with_info_id()
        bus.publish(self.domain_event)
        bus.configurer.clear()

    @testing_with_rabbitmq
    def should_publish_domain_event_with_previous_rabbitmq_configuration(self):
        configurer = RabbitMqMessageConfigurerMother.default()
        configurer.configure()

        bus = RabbitMqDomainEventBusMother.with_info_id()
        bus.publish(self.domain_event)

        configurer.clear()

    @testing_with_rabbitmq
    def should_publish_a_list_of_domain_events(self):
        events_number = 5
        domain_event_list = [
            DomainEventUserCreatedMother.random() for _ in range(events_number)
        ]

        configurer = RabbitMqMessageConfigurerMother.default()
        configurer.configure()

        bus = RabbitMqDomainEventBusMother.with_info_id()
        with mock.patch.object(
            BlockingChannel, "basic_publish"
        ) as mock_channel_publish:
            bus.publish_list(domain_event_list)

        assert mock_channel_publish.call_count == events_number

        configurer.clear()

    @testing_with_rabbitmq
    def should_publish_domain_event_only_on_store_queue_with_previous_rabbitmq_configuration(
        self,
    ):
        configurer = RabbitMqMessageConfigurerMother.default()
        configurer.configure()

        bus = RabbitMqDomainEventBusMother.with_info_id()
        bus.retry_publish_only_on_store_queue(self.domain_event)

        configurer.clear()

    @testing_with_rabbitmq
    def should_retry_publish_only_on_store_queue_not_affecting_default_domain_event_queue(
        self,
    ):

        spy_consumer_default_queue = SpyMessages()
        spy_consumer_store = SpyMessages()

        def assert_consumer_default_queue(domain_event: DomainEvent) -> BoolResult:
            spy_consumer_default_queue.append(domain_event)
            return isSuccess

        def assert_consumer_store(domain_event: DomainEvent) -> BoolResult:
            spy_consumer_store.append(domain_event)
            return isSuccess

        subscribers = [
            MessageSubscriberMother.domain_event_subscriber(
                domain_event_type=type(self.domain_event),
                handler=assert_consumer_default_queue,
            ),
            MessageSubscriberMother.all_messages_subscriber(
                handler=assert_consumer_store
            ),
        ]

        configurer = RabbitMqMessageConfigurerMother.default()
        configurer.configure_subscribers(subscribers)

        bus = RabbitMqDomainEventBusMother.with_info_id()
        bus.retry_publish_only_on_store_queue(self.domain_event)

        consumer = RabbitMqMessageConsumerMother.default()
        consumer.add_subscribers(subscribers)

        consumer.start()

        sleep(1.0)

        consumer.stop()
        configurer.clear()

        spy_consumer_default_queue.assert_number_unique_messages(0)
        spy_consumer_default_queue.assert_count_by_message_id(
            self.domain_event.message_id, 0
        )
        spy_consumer_store.assert_number_unique_messages(1)
        spy_consumer_store.assert_first_message(self.domain_event)
        spy_consumer_store.assert_count_by_message_id(self.domain_event.message_id, 1)

    @testing_with_rabbitmq
    def should_publish_and_then_consumer_retry_publish_only_on_store_queue_not_affecting_default_domain_event_queue(
        self,
    ):

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

        subscribers = [
            MessageSubscriberMother.domain_event_subscriber(
                domain_event_type=type(self.domain_event),
                handler=assert_consumer_default_queue,
            ),
            MessageSubscriberMother.all_messages_subscriber(
                handler=assert_consumer_store
            ),
        ]

        configurer = RabbitMqMessageConfigurerMother.default()
        configurer.configure_subscribers(subscribers)

        bus = RabbitMqDomainEventBusMother.default()
        bus.publish(self.domain_event)

        consumer = RabbitMqMessageConsumerMother.default()
        consumer.add_subscribers(subscribers)

        consumer.start()

        sleep(1.0)

        consumer.stop()
        configurer.clear()

        spy_consumer_default_queue.assert_count_by_message_id(
            self.domain_event.message_id, 1
        )
        spy_consumer_store.assert_count_by_message_id(self.domain_event.message_id, 2)

    @testing_with_rabbitmq
    def should_publish_via_fallback_when_unexpected_exception(self):

        mock_fallback_domain_event_bus = Mock(DomainEventBus)
        bus = RabbitMqDomainEventBusMother.default(
            fallback=mock_fallback_domain_event_bus
        )

        with patch.object(
            BlockingChannel, "basic_publish", side_effect=Exception()
        ) as mock_channel:
            bus.publish(self.domain_event)

            mock_fallback_domain_event_bus.publish.assert_called_once()
            mock_channel.assert_called_once()

        bus.configurer.clear()

    @testing_with_rabbitmq
    def should_publish_retry_and_publish_via_fallback_when_unexpected_exception(self):
        mock_fallback_domain_event_bus = Mock(DomainEventBus)
        bus = RabbitMqDomainEventBusMother.default(
            fallback=mock_fallback_domain_event_bus
        )

        with patch.object(
            BlockingChannel,
            "basic_publish",
            side_effect=ChannelClosedByBroker(reply_code=1, reply_text="dummy"),
        ) as mock_channel:
            bus.publish(self.domain_event)

            mock_fallback_domain_event_bus.publish.assert_called_once()
            assert mock_channel.call_count == 2
            assert bus.already_configured is True

        bus.configurer.clear()

    @testing_with_rabbitmq
    def should_publish_list_via_fallback_when_unexpected_exception(self):

        mock_fallback_domain_event_bus = Mock(DomainEventBus)
        bus = RabbitMqDomainEventBusMother.default(
            fallback=mock_fallback_domain_event_bus
        )

        with patch.object(
            BlockingChannel, "basic_publish", side_effect=Exception()
        ) as mock_channel:
            bus.publish_list([self.domain_event])

            mock_fallback_domain_event_bus.publish_list.assert_called_once()
            mock_channel.assert_called_once()

        bus.configurer.clear()

    @testing_with_rabbitmq
    def should_publish_list_retry_and_publish_via_fallback_when_unexpected_exception(
        self,
    ):
        mock_fallback_domain_event_bus = Mock(DomainEventBus)
        bus = RabbitMqDomainEventBusMother.default(
            fallback=mock_fallback_domain_event_bus
        )

        with patch.object(
            BlockingChannel,
            "basic_publish",
            side_effect=ChannelClosedByBroker(reply_code=1, reply_text="dummy"),
        ) as mock_channel:
            bus.publish_list([self.domain_event])

            mock_fallback_domain_event_bus.publish_list.assert_called_once()
            assert mock_channel.call_count == 2
            assert bus.already_configured is True

        bus.configurer.clear()
