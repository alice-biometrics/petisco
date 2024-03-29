from time import sleep

import pytest
from meiga import BoolResult, isSuccess

from petisco import Command, DomainEvent
from petisco.extra.rabbitmq import RabbitMqCommandBus, RabbitMqDomainEventBus
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
    @testing_with_rabbitmq
    def should_publish_a_domain_event_and_a_command_on_consumer(self):
        spy = SpyMessages()
        spy_derived_domain_event = SpyMessages()
        spy_command = SpyMessages()

        domain_event = DomainEventUserCreatedMother.random()
        derived_domain_event = DomainEventUserUpdatedMother.random()
        command = CommandPersistUserMother.random()

        def assert_consumer(self, domain_event: DomainEvent) -> BoolResult:
            spy.append(domain_event)

            assert isinstance(self.domain_event_bus, RabbitMqDomainEventBus)
            assert isinstance(self.command_bus, RabbitMqCommandBus)

            self.domain_event_bus.publish(DomainEventUserUpdatedMother.random())
            self.command_bus.dispatch(CommandPersistUserMother.random())
            return isSuccess

        def assert_consumer_derived_domain_event(
            domain_event: DomainEvent,
        ) -> BoolResult:
            spy_derived_domain_event.append(domain_event)
            return isSuccess

        def assert_consumer_command(command: Command) -> BoolResult:
            spy_command.append(command)
            return isSuccess

        subscribers = [
            MessageSubscriberMother.domain_event_subscriber_with_self_handler(
                domain_event_type=type(domain_event), self_handler=assert_consumer
            ),
            MessageSubscriberMother.other_domain_event_subscriber(
                domain_event_type=type(derived_domain_event),
                handler=assert_consumer_derived_domain_event,
            ),
            MessageSubscriberMother.command_subscriber(
                command_type=type(command), handler=assert_consumer_command
            ),
        ]

        configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
        configurer.configure_subscribers(subscribers)

        consumer = RabbitMqMessageConsumerMother.with_max_retries(1)
        consumer.add_subscribers(subscribers)
        consumer.start()

        bus = RabbitMqDomainEventBusMother.default()
        bus.publish(domain_event)

        sleep(1.0)

        consumer.stop()
        configurer.clear()

        spy.assert_number_unique_messages(1)
        spy_derived_domain_event.assert_number_unique_messages(1)
        spy_command.assert_number_unique_messages(1)
