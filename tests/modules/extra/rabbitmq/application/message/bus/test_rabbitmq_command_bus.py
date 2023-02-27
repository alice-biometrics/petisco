from time import sleep
from unittest.mock import Mock, patch

import pytest
from meiga import BoolResult, isSuccess
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import ChannelClosedByBroker

from petisco import Command, CommandBus, DomainEvent
from tests.modules.extra.rabbitmq.mother.command_persist_user_mother import (
    CommandPersistUserMother,
)
from tests.modules.extra.rabbitmq.mother.message_subscriber_mother import (
    MessageSubscriberMother,
)
from tests.modules.extra.rabbitmq.mother.rabbitmq_command_bus_mother import (
    RabbitMqCommandBusMother,
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
class TestRabbitMqCommandBus:
    command: Command

    def setup_method(self):
        self.command = CommandPersistUserMother.random()

    @testing_with_rabbitmq
    def should_dispatch_command_without_rabbitmq_configuration(self):
        bus = RabbitMqCommandBusMother.default()
        bus.dispatch(self.command)

        bus.configurer.clear()

    @testing_with_rabbitmq
    def should_dispatch_command_without_rabbitmq_configuration_and_info_id(self):
        bus = RabbitMqCommandBusMother.with_info_id()
        bus.dispatch(self.command)
        bus.configurer.clear()

    @testing_with_rabbitmq
    def should_dispatch_command_with_previous_rabbitmq_configuration(self):
        configurer = RabbitMqMessageConfigurerMother.default()
        configurer.configure()

        bus = RabbitMqCommandBusMother.with_info_id()
        bus.dispatch(self.command)

        configurer.clear()

    @testing_with_rabbitmq
    def should_dispatch_command_with_a_command_subscriber(self):
        spy_consumer_default_queue = SpyMessages()
        spy_consumer_store = SpyMessages()

        def assert_consumer_default_queue(domain_event: DomainEvent) -> BoolResult:
            spy_consumer_default_queue.append(domain_event)
            return isSuccess

        def assert_consumer_store(domain_event: DomainEvent) -> BoolResult:
            spy_consumer_store.append(domain_event)
            return isSuccess

        subscribers = [
            MessageSubscriberMother.command_subscriber(
                command_type=type(self.command), handler=assert_consumer_default_queue
            ),
            MessageSubscriberMother.all_messages_subscriber(
                handler=assert_consumer_store
            ),
        ]

        configurer = RabbitMqMessageConfigurerMother.default()
        configurer.configure_subscribers(subscribers)

        bus = RabbitMqCommandBusMother.default()
        bus.dispatch(self.command)

        consumer = RabbitMqMessageConsumerMother.default()
        consumer.add_subscribers(subscribers)

        consumer.start()

        sleep(1.0)

        consumer.stop()
        configurer.clear()

        spy_consumer_default_queue.assert_count_by_message_id(
            self.command.message_id, 1
        )
        spy_consumer_store.assert_count_by_message_id(self.command.message_id, 1)

    @testing_with_rabbitmq
    def should_dispatch_via_fallback_when_unexpected_exception(self):
        mock_fallback_command_bus = Mock(CommandBus)
        bus = RabbitMqCommandBusMother.default(fallback=mock_fallback_command_bus)

        with patch.object(
            BlockingChannel, "basic_publish", side_effect=Exception()
        ) as mock_channel:
            bus.dispatch(self.command)

            mock_fallback_command_bus.dispatch.assert_called_once()
            mock_channel.assert_called_once()

        bus.configurer.clear()

    @testing_with_rabbitmq
    def should_dispatch_retry_and_dispatch_via_fallback_when_unexpected_exception(self):
        mock_fallback_command_bus = Mock(CommandBus)
        bus = RabbitMqCommandBusMother.default(fallback=mock_fallback_command_bus)

        with patch.object(
            BlockingChannel,
            "basic_publish",
            side_effect=ChannelClosedByBroker(reply_code=1, reply_text="dummy"),
        ) as mock_channel:
            bus.dispatch(self.command)

            mock_fallback_command_bus.dispatch.assert_called_once()
            assert mock_channel.call_count == 2
            assert bus.already_configured is True

        bus.configurer.clear()
