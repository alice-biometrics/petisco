from time import sleep

import pytest
from meiga import isSuccess, isFailure, Result, Error

from petisco import DomainEvent
from petisco.extra.rabbitmq import SpecificQueueConfig
from petisco.legacy.fixtures import testing_with_rabbitmq
from tests.modules.extra.rabbitmq.mother.domain_event_user_created_mother import (
    DomainEventUserCreatedMother,
)
from tests.modules.extra.rabbitmq.mother.message_subscriber_mother import (
    MessageSubscriberMother,
)
from tests.modules.extra.rabbitmq.mother.queue_config_mother import QueueConfigMother
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
@pytest.mark.parametrize(
    "max_retries_allowed,expected_number_event_consumed,simulated_results",
    [
        (0, 1, [isFailure]),
        (1, 2, [isFailure, isSuccess]),
        (2, 3, [isFailure, isFailure, isSuccess]),
        (3, 4, [isFailure, isFailure, isFailure, isSuccess]),
        (4, 5, [isFailure, isFailure, isFailure, isFailure, isSuccess]),
    ],
)
def test_message_consumer_should_publish_consume_and_retry_event_from_rabbitmq_when_a_queue_is_configured_with_specific_parameters(
    max_retries_allowed, expected_number_event_consumed, simulated_results
):
    spy = SpyMessages()
    spy_specific = SpyMessages()

    def assert_consumer(domain_event: DomainEvent) -> Result[bool, Error]:
        spy.append(domain_event)
        result = simulated_results.pop(0)
        return result

    def assert_specific_consumer(domain_event: DomainEvent) -> Result[bool, Error]:
        spy_specific.append(domain_event)
        return isSuccess

    domain_event = DomainEventUserCreatedMother.random()
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer
        ),
        MessageSubscriberMother.other_domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_specific_consumer
        ),
    ]

    specific_queue_config = SpecificQueueConfig(
        wildcard="*assert_specific_consumer",
        specific_retry_ttl=50,
        specific_main_ttl=75,
    )
    queue_config = QueueConfigMother.with_specific_queue_config(
        specific_queue_config, default_retry_ttl=100, default_main_ttl=100
    )

    configurer = RabbitMqMessageConfigurerMother.with_queue_config(queue_config)
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    consumer = RabbitMqMessageConsumerMother.with_max_retries(max_retries_allowed)
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_messages(1)
    spy.assert_first_message(domain_event)
    spy.assert_last_message(domain_event)
    spy.assert_count_by_message_id(
        domain_event.message_id, expected_number_event_consumed
    )
    spy_specific.assert_number_unique_messages(1)
