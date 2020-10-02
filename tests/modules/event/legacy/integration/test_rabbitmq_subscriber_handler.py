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
    RabbitMqConnector,
    RoutingKey,
    ERROR,
    WARNING,
)

from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_is_running_locally import (
    rabbitmq_is_running_locally,
)
from tests.fixtures import TrackedEventsSpy
from tests.modules.unit.mocks.fake_logger import FakeLogger
from tests.modules.unit.mocks.log_message_mother import LogMessageMother


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
    def _given_any_publisher_and_subscriber(
        subscriber_handler: Callable,
        organization: str = None,
        service: str = None,
        topic: str = None,
    ):

        organization = organization if organization else given_random_organization
        service = service if service else given_random_service
        topic = topic if topic else given_random_topic

        publisher = given_any_publisher(organization, service, topic)
        subscriber = given_any_subscriber(
            organization, service, topic, subscriber_handler
        )
        return publisher, subscriber

    return _given_any_publisher_and_subscriber


@pytest.fixture
def given_any_publisher():
    def _given_any_publisher(
        given_random_organization, given_random_service, given_random_topic
    ):
        publisher = RabbitMQEventPublisher(
            connector=RabbitMqConnector(),
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
            connector=RabbitMqConnector(),
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
    given_any_petisco, make_user_created_event, given_any_publisher_and_subscriber
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
    given_any_petisco, make_user_created_event, given_any_publisher_and_subscriber
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
        WARNING,
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
    given_any_petisco, make_user_created_event, given_any_publisher_and_subscriber
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
        WARNING,
        LogMessageMother.get_subscriber(
            operation="main_handler",
            message=f"Message rejected (filtering by routing_key {invalid_routing_key})",
        ).to_dict(),
    )
    subscriber.stop()


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_subscriber_handler_receive_one_event_and_obtain_the_routing_key(
    given_any_petisco, make_user_created_event, given_any_publisher_and_subscriber
):
    event = make_user_created_event()
    tracked_events_spy = TrackedEventsSpy()
    expected_organization = "acmeorganization"

    @subscriber_handler()
    def main_handler(event: Event, routing_key: RoutingKey):
        assert routing_key.match(organization=expected_organization)
        tracked_events_spy.append(event)
        return isSuccess

    publisher, subscriber = given_any_publisher_and_subscriber(
        main_handler, organization=expected_organization
    )

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
def test_should_subscriber_handler_return_a_failure_with_unknown_error_when_raise_an_uncontrolled_exception(
    given_any_petisco, make_user_created_event, given_any_publisher_and_subscriber
):
    event = make_user_created_event()
    expected_organization = "acmeorganization"

    logger = FakeLogger()

    @subscriber_handler(logger=logger)
    def main_handler(event: Event, routing_key: RoutingKey):
        raise RuntimeError("uncontrolled exception")

    publisher, subscriber = given_any_publisher_and_subscriber(
        main_handler, organization=expected_organization
    )

    subscriber.start()

    await_for_subscriber()

    publisher.publish(event)

    await_for_events()

    subscriber.stop()

    second_logging_message = logger.get_logging_messages()[1]
    assert second_logging_message[0] == ERROR
    assert (
        "Result[status: failure | value: UnknownError (main_handler (Subscriber)): RuntimeError: uncontrolled exception."
        in second_logging_message[1]["data"]["message"]
    )
    assert "Input Parameters:" in second_logging_message[1]["data"]["message"]
