from unittest import mock
from unittest.mock import Mock, patch

import pytest
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import ChannelClosedByBroker

from petisco import DomainEvent, DomainEventBus
from tests.modules.extra.rabbitmq.mother.domain_event_user_created_mother import (
    DomainEventUserCreatedMother,
)
from tests.modules.extra.rabbitmq.mother.rabbitmq_domain_event_bus_mother import (
    RabbitMqDomainEventBusMother,
)
from tests.modules.extra.rabbitmq.mother.rabbitmq_message_configurer_mother import (
    RabbitMqMessageConfigurerMother,
)
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
        domain_event_list = [DomainEventUserCreatedMother.random() for _ in range(events_number)]

        configurer = RabbitMqMessageConfigurerMother.default()
        configurer.configure()

        bus = RabbitMqDomainEventBusMother.with_info_id()
        with mock.patch.object(BlockingChannel, "basic_publish") as mock_channel_publish:
            bus.publish(domain_event_list)

        assert mock_channel_publish.call_count == events_number

        configurer.clear()

    @testing_with_rabbitmq
    def should_publish_via_fallback_when_unexpected_exception(self):
        mock_fallback_domain_event_bus = Mock(DomainEventBus)
        bus = RabbitMqDomainEventBusMother.default(fallback=mock_fallback_domain_event_bus)

        with patch.object(BlockingChannel, "basic_publish", side_effect=Exception()) as mock_channel:
            bus.publish(self.domain_event)

            mock_fallback_domain_event_bus.publish.assert_called_once()
            mock_channel.assert_called_once()

        bus.configurer.clear()

    @testing_with_rabbitmq
    def should_publish_retry_and_publish_via_fallback_when_unexpected_exception(self):
        mock_fallback_domain_event_bus = Mock(DomainEventBus)
        bus = RabbitMqDomainEventBusMother.default(fallback=mock_fallback_domain_event_bus)

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
        bus = RabbitMqDomainEventBusMother.default(fallback=mock_fallback_domain_event_bus)

        with patch.object(BlockingChannel, "basic_publish", side_effect=Exception()) as mock_channel:
            bus.publish([self.domain_event])

            mock_fallback_domain_event_bus.publish.assert_called_once()
            mock_channel.assert_called_once()

        bus.configurer.clear()

    @testing_with_rabbitmq
    def should_publish_list_retry_and_publish_via_fallback_when_unexpected_exception(
        self,
    ):
        mock_fallback_domain_event_bus = Mock(DomainEventBus)
        bus = RabbitMqDomainEventBusMother.default(fallback=mock_fallback_domain_event_bus)

        with patch.object(
            BlockingChannel,
            "basic_publish",
            side_effect=ChannelClosedByBroker(reply_code=1, reply_text="dummy"),
        ) as mock_channel:
            bus.publish([self.domain_event])

            mock_fallback_domain_event_bus.publish.assert_called_once()
            assert mock_channel.call_count == 2
            assert bus.already_configured is True

        bus.configurer.clear()

    @testing_with_rabbitmq
    def should_raise_an_unexpected_exception_when_not_given_fallback_when_publish(self):
        bus = RabbitMqDomainEventBusMother.default()

        with patch.object(BlockingChannel, "basic_publish", side_effect=Exception()) as mock_channel:
            with pytest.raises(Exception):
                bus.publish(self.domain_event)

            mock_channel.assert_called_once()

        bus.configurer.clear()

    @testing_with_rabbitmq
    def should_raise_an_unexpected_exception_when_not_given_fallback_when_publish_list(
        self,
    ):
        bus = RabbitMqDomainEventBusMother.default()

        with patch.object(BlockingChannel, "basic_publish", side_effect=Exception()) as mock_channel:
            with pytest.raises(Exception):
                bus.publish([self.domain_event])

            mock_channel.assert_called_once()

        bus.configurer.clear()
