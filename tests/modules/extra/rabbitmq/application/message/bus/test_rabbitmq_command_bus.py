from time import sleep

import pytest
from meiga import BoolResult, isSuccess

from petisco import DomainEvent
from petisco.legacy.fixtures.testing_decorators import testing_with_rabbitmq
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


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_command_bus_should_dispatch_command_without_rabbitmq_configuration():
    command = CommandPersistUserMother.random()

    bus = RabbitMqCommandBusMother.default()
    bus.dispatch(command)

    bus.configurer.clear()


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_command_bus_should_dispatch_command_without_rabbitmq_configuration_and_info_id():
    command = CommandPersistUserMother.random()

    bus = RabbitMqCommandBusMother.with_info_id()
    bus.dispatch(command)
    bus.configurer.clear()


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_command_bus_should_dispatch_command_with_previous_rabbitmq_configuration():
    command = CommandPersistUserMother.random()

    configurer = RabbitMqMessageConfigurerMother.default()
    configurer.configure()

    bus = RabbitMqCommandBusMother.with_info_id()
    bus.dispatch(command)

    configurer.clear()


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_command_bus_dispatch_command_with_a_command_subscriber():

    spy_consumer_default_queue = SpyMessages()
    spy_consumer_store = SpyMessages()

    def assert_consumer_default_queue(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_default_queue.append(domain_event)
        return isSuccess

    def assert_consumer_store(domain_event: DomainEvent) -> BoolResult:
        spy_consumer_store.append(domain_event)
        return isSuccess

    command = CommandPersistUserMother.random()

    subscribers = [
        MessageSubscriberMother.command_subscriber(
            command_type=type(command), handler=assert_consumer_default_queue
        ),
        MessageSubscriberMother.all_messages_subscriber(handler=assert_consumer_store),
    ]

    configurer = RabbitMqMessageConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqCommandBusMother.default()
    bus.dispatch(command)

    consumer = RabbitMqMessageConsumerMother.default()
    consumer.add_subscribers(subscribers)

    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy_consumer_default_queue.assert_count_by_message_id(command.message_id, 1)
    spy_consumer_store.assert_count_by_message_id(command.message_id, 1)
