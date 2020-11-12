from time import sleep

import pytest
from meiga import isSuccess, isFailure, Result, Error

from petisco import Event
from petisco.event.queue.domain.specific_queue_config import SpecificQueueConfig
from petisco.event.shared.domain.event_subscriber import EventSubscriber

from petisco.fixtures.testing_decorators import testing_with_rabbitmq
from tests.modules.event.mothers.event_user_created_mother import EventUserCreatedMother
from tests.modules.event.mothers.queue_config_mother import QueueConfigMother
from tests.modules.event.mothers.rabbitmq_event_bus_mother import RabbitMqEventBusMother
from tests.modules.event.mothers.rabbitmq_event_configurer_mother import (
    RabbitMqEventConfigurerMother,
)
from tests.modules.event.mothers.rabbitmq_event_consumer_mother import (
    RabbitMqEventConsumerMother,
)
from tests.modules.event.spies.spy_events import SpyEvents


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
def test_should_publish_consume_and_retry_event_from_rabbitmq_when_a_queue_is_configured_with_specific_parameters(
    max_retries_allowed, expected_number_event_consumed, simulated_results
):
    spy = SpyEvents()
    spy_specific = SpyEvents()

    def assert_consumer(event: Event) -> Result[bool, Error]:
        spy.append(event)
        result = simulated_results.pop(0)
        return result

    def assert_specific_consumer(event: Event) -> Result[bool, Error]:
        spy_specific.append(event)
        return isSuccess

    event = EventUserCreatedMother.random()
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer, assert_specific_consumer],
        )
    ]

    specific_queue_config = SpecificQueueConfig(
        wildcard="*assert_specific_consumer",
        specific_retry_ttl=50,
        specific_main_ttl=75,
    )
    queue_config = QueueConfigMother.with_specific_queue_config(
        specific_queue_config, default_retry_ttl=100, default_main_ttl=100
    )

    configurer = RabbitMqEventConfigurerMother.with_queue_config(queue_config)
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(max_retries_allowed)
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_last_event(event)
    spy.assert_count_by_event_id(event.event_id, expected_number_event_consumed)
    spy_specific.assert_number_unique_events(1)
