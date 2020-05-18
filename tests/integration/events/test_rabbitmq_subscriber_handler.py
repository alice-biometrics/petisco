from time import sleep
from typing import Callable

import pytest
from meiga import isSuccess

from petisco import (
    Event,
    subscriber_handler,
    RabbitMQEventPublisher,
    RabbitMQEventSubscriber,
    ConfigEventSubscriber,
    RabbitMQConnector,
    INFO,
)

from petisco.events.rabbitmq.rabbitmq_is_running_locally import (
    rabbitmq_is_running_locally,
)
from tests.fixtures import TrackedEventsSpy
from tests.unit.mocks.fake_logger import FakeLogger
from tests.unit.mocks.log_message_mother import LogMessageMother


def await_for_subscriber():
    sleep(2.0)


def await_for_events():
    sleep(1.5)


@pytest.fixture
def given_any_publisher_and_subscriber(
    given_any_publisher,
    given_any_subscriber,
    given_random_organization,
    given_random_service,
    given_random_topic,
):
    def _given_any_publisher_and_subscriber(subscriber_handler: Callable):
        publisher = given_any_publisher(
            given_random_organization, given_random_service, given_random_topic
        )
        subscriber = given_any_subscriber(
            given_random_organization,
            given_random_service,
            given_random_topic,
            subscriber_handler,
        )
        return publisher, subscriber

    return _given_any_publisher_and_subscriber


@pytest.fixture
def given_any_publisher():
    def _given_any_publisher(
        given_random_organization, given_random_service, given_random_topic
    ):
        publisher = RabbitMQEventPublisher(
            connector=RabbitMQConnector(),
            organization=given_random_organization,
            service=given_random_service,
            topic=given_random_topic,
        )
        return publisher

    return _given_any_publisher


@pytest.fixture
def given_any_subscriber():
    def _given_any_subscriber(
        given_random_organization,
        given_random_service,
        given_random_topic,
        subscriber_handler: Callable,
    ):
        subscriber = RabbitMQEventSubscriber(
            connector=RabbitMQConnector(),
            subscribers={
                "petisco": ConfigEventSubscriber(
                    organization=given_random_organization,
                    service=given_random_service,
                    topic=given_random_topic,
                    handler=subscriber_handler,
                )
            },
        )
        return subscriber

    return _given_any_subscriber


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_subscriber_handler_receive_one_event(
    make_user_created_event, given_any_publisher_and_subscriber
):
    event = make_user_created_event()
    tracked_events_spy = TrackedEventsSpy()

    @subscriber_handler()
    def main_handler(event: Event):
        tracked_events_spy.append(event)
        return isSuccess

    publisher, subscriber = given_any_publisher_and_subscriber(main_handler)

    subscriber.start()

    await_for_subscriber()

    publisher.publish(event)

    await_for_events()

    tracked_events_spy.assert_number_events(1)

    subscriber.stop()


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_subscriber_handler_always_simulate_a_nack(
    make_user_created_event, given_any_publisher_and_subscriber
):
    logger = FakeLogger()
    event = make_user_created_event()
    tracked_events_spy = TrackedEventsSpy()

    @subscriber_handler(logger=logger, percentage_simulate_nack=1.0)
    def main_handler(event: Event):
        tracked_events_spy.append(event)
        return isSuccess

    publisher, subscriber = given_any_publisher_and_subscriber(main_handler)

    subscriber.start()

    await_for_subscriber()

    publisher.publish(event)

    await_for_events()

    tracked_events_spy.assert_number_events(0)

    second_logging_message = logger.get_logging_messages()[1]

    assert second_logging_message == (
        INFO,
        LogMessageMother.get_subscriber(
            operation="main_handler",
            message="Message rejected (Simulation rejecting 100.0% of the messages)",
        ).to_dict(),
    )

    subscriber.stop()


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_subscriber_handler_always_returns_nack_filtering_by_invalid_routing_key(
    make_user_created_event, given_any_publisher_and_subscriber
):
    logger = FakeLogger()
    event = make_user_created_event()
    tracked_events_spy = TrackedEventsSpy()
    invalid_routing_key = "invalid.routing.key"

    @subscriber_handler(logger=logger, filter_routing_key=invalid_routing_key)
    def main_handler(event: Event):
        tracked_events_spy.append(event)
        return isSuccess

    publisher, subscriber = given_any_publisher_and_subscriber(main_handler)

    subscriber.start()

    await_for_subscriber()

    publisher.publish(event)

    await_for_events()

    tracked_events_spy.assert_number_events(0)

    second_logging_message = logger.get_logging_messages()[1]

    assert second_logging_message == (
        INFO,
        LogMessageMother.get_subscriber(
            operation="main_handler",
            message=f"Message rejected (filtering by routing_key {invalid_routing_key})",
        ).to_dict(),
    )
    subscriber.stop()
