from time import sleep

import pytest
from meiga import isSuccess, isFailure, BoolResult

from petisco import Event, subscriber_handler

from petisco.fixtures.testing_decorators import testing_with_rabbitmq
from petisco.logger.not_implemented_logger import NotImplementedLogger
from tests.modules.event.legacy.mothers.rabbitmq_event_publisher_mother import (
    RabbitMqEventPublisherMother,
)
from tests.modules.event.legacy.mothers.rabbitmq_event_subscriber_mother import (
    RabbitMqEventSubscriberMother,
)
from tests.modules.event.legacy.mothers.rabbitmq_queue_naming_mother import (
    RabbitMqQueueNamingMother,
)
from tests.modules.event.mothers.event_user_created_mother import EventUserCreatedMother
from tests.modules.event.mothers.rabbitmq_declarer_mother import RabbitMqDeclarerMother

from tests.modules.event.mothers.rabbitmq_event_consumer_mother import (
    RabbitMqEventConsumerMother,
)
from tests.modules.event.spies.spy_events import SpyEvents


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_configure_one_services_with_modern_event_management_an_other_with_legacy():
    spy_legacy = SpyEvents()
    spy_modern = SpyEvents()
    event = EventUserCreatedMother.random()

    def step_1_execute_legacy():
        # Define legacy Subscriber
        @subscriber_handler(logger=NotImplementedLogger())
        def main_handler(event: Event):
            spy_legacy.append(event)
            return isFailure

        subscriber = RabbitMqEventSubscriberMother.default(main_handler)
        subscriber.start()

        # Define legacy Publisher
        legacy_publisher = RabbitMqEventPublisherMother.default()
        legacy_publisher.publish(event)

        sleep(1.0)

        subscriber.stop()

    def step_2_execute_modern():
        # Define modern Consumer
        def modern_handler(event: Event) -> BoolResult:
            spy_modern.append(event)
            return isSuccess

        legacy_queue = RabbitMqQueueNamingMother.legacy_dead_letter_queue()
        consumer = RabbitMqEventConsumerMother.default()
        consumer.add_handler_on_queue(legacy_queue, modern_handler)
        consumer.start()

        sleep(1.0)

        consumer.stop()

    rabbitmq = RabbitMqDeclarerMother.default()
    rabbitmq.delete_queue(RabbitMqQueueNamingMother.legacy_dead_letter_queue())

    step_1_execute_legacy()
    step_2_execute_modern()

    spy_legacy.assert_number_unique_events(1)
    spy_legacy.assert_first_event(event)

    spy_modern.assert_number_unique_events(1)
    spy_modern.assert_first_event(event)
    spy_modern.assert_count_by_event_id(event.event_id, 1)

    rabbitmq.delete_queue(RabbitMqQueueNamingMother.legacy_main_queue())
    rabbitmq.delete_queue(RabbitMqQueueNamingMother.legacy_dead_letter_queue())
