from time import sleep
from unittest.mock import Mock

import pytest
from meiga import BoolResult, isSuccess

from petisco import CommandBus, DomainEvent, DomainEventBus
from tests.modules.extra.rabbitmq.mother.command_persist_user_mother import (
    CommandPersistUserMother,
)
from tests.modules.extra.rabbitmq.mother.domain_event_user_created_mother import (
    DomainEventUserCreatedMother,
)
from tests.modules.extra.rabbitmq.mother.domain_event_user_updated_mother import (
    DomainEventUserUpdatedMother,
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
class TestRabbitMqMessageConsumerPublishing:
    mock_domain_event_bus: Mock
    mock_command_bus: Mock

    def setup_method(self):
        self.mock_domain_event_bus = Mock(DomainEventBus)
        self.mock_domain_event_bus.publish = Mock(return_value=None)
        self.mock_command_bus = Mock(CommandBus)
        self.mock_command_bus.dispatch = Mock(return_value=None)

    @testing_with_rabbitmq
    def should_publish_a_domain_event_with_external_bus_from_builder(self):
        spy = SpyMessages()

        domain_event = DomainEventUserCreatedMother.random()

        def assert_consumer(self, domain_event: DomainEvent) -> BoolResult:
            spy.append(domain_event)

            assert isinstance(self.domain_event_bus, Mock)
            assert isinstance(self.command_bus, Mock)

            self.domain_event_bus.publish(DomainEventUserUpdatedMother.random())
            self.command_bus.dispatch(CommandPersistUserMother.random())
            return isSuccess

        subscribers = [
            MessageSubscriberMother.domain_event_subscriber_with_self_handler(
                domain_event_type=type(domain_event), self_handler=assert_consumer
            )
        ]

        configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
        configurer.configure_subscribers(subscribers)

        def domain_event_bus_builder() -> DomainEventBus:
            return self.mock_domain_event_bus

        def command_bus_builder() -> CommandBus:
            return self.mock_command_bus

        consumer = RabbitMqMessageConsumerMother.with_bus_builders(
            domain_event_bus_builder, command_bus_builder, 1
        )
        consumer.add_subscribers(subscribers)
        consumer.start()

        bus = RabbitMqDomainEventBusMother.default()
        bus.publish(domain_event)

        sleep(1.0)

        consumer.stop()
        configurer.clear()

        spy.assert_number_unique_messages(1)

        self.mock_domain_event_bus.publish.assert_called()
        self.mock_command_bus.dispatch.assert_called()
