from typing import Callable

from time import sleep

import pytest

from petisco.events.publisher.infrastructure.rabbitmq_event_publisher import (
    RabbitMQEventPublisher,
)
from petisco.events.rabbitmq.rabbitmq_connector import RabbitMQConnector
from petisco.events.subscriber.domain.config_event_subscriber import (
    ConfigEventSubscriber,
)

from petisco.events.rabbitmq.rabbitmq_is_running_locally import (
    rabbitmq_is_running_locally,
)
from petisco.events.subscriber.domain.subscriber_handler import subscriber_handler
from petisco.events.subscriber.infrastructure.rabbitmq_event_subscriber import (
    RabbitMQEventSubscriber,
)

from petisco.events.event import Event
from meiga import isSuccess

from tests.fixtures import TrackedEventsSpy


def await_for_it(seconds: float = 1.5):
    sleep(seconds)


@pytest.fixture()
def given_any_config_event_subscriber(
    given_random_organization, given_random_service, given_random_topic
):
    def _given_any_config_event_subscriber(
        handler: Callable = lambda ch, method, properties, body: None,
    ):
        return ConfigEventSubscriber(
            organization=given_random_organization,
            service=given_random_service,
            topic=given_random_topic,
            handler=handler,
        )

    return _given_any_config_event_subscriber


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_create_a_rabbitmq_event_subscriber_and_then_close_it(
    given_any_config_event_subscriber
):
    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMQConnector(),
        subscribers={"auth": given_any_config_event_subscriber()},
    )
    subscriber.start()

    await_for_it()

    info = subscriber.info()

    assert info == {
        "name": "RabbitMQEventSubscriber",
        "connection.is_open": True,
        "subscribers_status": {"auth": "subscribed"},
    }

    subscriber.stop()


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_create_a_rabbitmq_event_subscriber_and_then_unsubscribe_all_when_not_subscribe_all_before(
    given_any_config_event_subscriber
):
    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMQConnector(),
        subscribers={"auth": given_any_config_event_subscriber()},
    )
    subscriber.stop()


@pytest.mark.integration
def test_should_fail_subscriber_when_connection_parameter_are_not_valid(
    given_any_config_event_subscriber
):
    with pytest.raises(TypeError):
        _ = RabbitMQEventSubscriber(
            connector=None, subscribers={"auth": given_any_config_event_subscriber()}
        )


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_create_a_rabbitmq_event_subscriber_and_check_info(
    given_any_config_event_subscriber
):
    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMQConnector(),
        subscribers={"auth": given_any_config_event_subscriber()},
    )
    info = subscriber.info()

    assert info == {
        "name": "RabbitMQEventSubscriber",
        "connection.is_open": False,
        "subscribers_status": {},
    }
    subscriber.stop()


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_throw_a_exception_if_try_to_start_a_subscriber_with_no_subscribers():
    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMQConnector(), subscribers=None
    )

    with pytest.raises(RuntimeError):
        subscriber.start()


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_create_two_rabbitmq_event_subscriber_and_then_close_one_without_altering_the_other(
    given_any_config_event_subscriber
):
    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMQConnector(),
        subscribers={"auth": given_any_config_event_subscriber()},
        connection_name="subscriber",
    )
    dl_subscriber = RabbitMQEventSubscriber(
        connector=RabbitMQConnector(),
        subscribers={"dl-auth": given_any_config_event_subscriber()},
        connection_name="dl-subscriber",
    )

    subscriber.start()
    dl_subscriber.start()

    await_for_it()

    assert subscriber.info() == {
        "name": "RabbitMQEventSubscriber",
        "connection.is_open": True,
        "subscribers_status": {"auth": "subscribed"},
    }

    assert dl_subscriber.info() == {
        "name": "RabbitMQEventSubscriber",
        "connection.is_open": True,
        "subscribers_status": {"dl-auth": "subscribed"},
    }

    dl_subscriber.stop()

    await_for_it(4.0)

    assert subscriber.info() == {
        "name": "RabbitMQEventSubscriber",
        "connection.is_open": True,
        "subscribers_status": {"auth": "subscribed"},
    }

    assert dl_subscriber.info() == {
        "name": "RabbitMQEventSubscriber",
        "connection.is_open": True,
        "subscribers_status": {"dl-auth": "unsubscribed"},
    }
    subscriber.stop()


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_work_successfully_a_happy_path_pub_sub_with_two_subscribers_and_closing_one_of_them(
    make_user_created_event,
    given_random_organization,
    given_random_service,
    given_random_topic,
):
    event_1 = make_user_created_event()
    event_2 = make_user_created_event()

    global tracked_events_spy
    tracked_events_spy = TrackedEventsSpy()

    global tracked_requeue_events_dead_letter_spy
    tracked_requeue_events_dead_letter_spy = TrackedEventsSpy()

    @subscriber_handler()
    def main_handler(event: Event):
        global tracked_events_spy
        tracked_events_spy.append(event)
        return isSuccess

    @subscriber_handler()
    def main_handler_requeue(event: Event):
        global tracked_requeue_events_dead_letter_spy
        tracked_requeue_events_dead_letter_spy.append(event)
        return isSuccess

    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMQConnector(),
        subscribers={
            "auth": ConfigEventSubscriber(
                organization=given_random_organization,
                service=given_random_service,
                topic=given_random_topic,
                handler=main_handler,
            )
        },
        connection_name="subscriber",
    )
    dl_subscriber = RabbitMQEventSubscriber(
        connector=RabbitMQConnector(),
        subscribers={
            "dl-auth": ConfigEventSubscriber(
                organization=given_random_organization,
                service=given_random_service,
                topic=given_random_topic,
                handler=main_handler_requeue,
            )
        },
        connection_name="dl-subscriber",
    )

    publisher = RabbitMQEventPublisher(
        connector=RabbitMQConnector(),
        organization=given_random_organization,
        service=given_random_service,
        topic=given_random_topic,
    )

    subscriber.start()
    dl_subscriber.start()

    await_for_it(4.5)

    publisher.publish(event_1)

    await_for_it(3.0)

    print(tracked_events_spy.events)
    tracked_events_spy.assert_number_events(1)
    tracked_requeue_events_dead_letter_spy.assert_number_events(0)

    dl_subscriber.stop()

    publisher.publish(event_2)

    await_for_it(3.5)

    tracked_events_spy.assert_number_events(2)
    tracked_requeue_events_dead_letter_spy.assert_number_events(0)

    print(tracked_events_spy.events)

    subscriber.stop()
