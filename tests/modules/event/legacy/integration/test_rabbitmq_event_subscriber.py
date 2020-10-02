from typing import Callable

from time import sleep

import pytest
import os

from petisco.event.legacy.publisher.infrastructure.rabbitmq_event_publisher import (
    RabbitMQEventPublisher,
)
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_connector import (
    RabbitMqConnector,
)
from petisco.event.legacy.subscriber.domain.config_event_subscriber import (
    ConfigEventSubscriber,
)

from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_is_running_locally import (
    rabbitmq_is_running_locally,
)
from petisco.event.legacy.subscriber.domain.subscriber_handler import subscriber_handler
from petisco.event.legacy.subscriber.infrastructure.rabbitmq_event_subscriber import (
    RabbitMQEventSubscriber,
)

from petisco.event.shared.domain.event import Event
from meiga import isSuccess


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
        connector=RabbitMqConnector(),
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
def test_should_create_a_rabbitmq_event_subscriber_and_try_to_delete_twice(
    given_any_config_event_subscriber
):
    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMqConnector(),
        subscribers={"auth": given_any_config_event_subscriber()},
    )
    subscriber.start()
    await_for_it()
    subscriber.stop()
    subscriber.stop()


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_create_a_rabbitmq_event_subscriber_and_then_unsubscribe_all_when_not_subscribe_all_before(
    given_any_config_event_subscriber
):
    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMqConnector(),
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
        connector=RabbitMqConnector(),
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
        connector=RabbitMqConnector(), subscribers=None
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
        connector=RabbitMqConnector(),
        subscribers={"auth": given_any_config_event_subscriber()},
        connection_name="subscriber",
    )
    dl_subscriber = RabbitMQEventSubscriber(
        connector=RabbitMqConnector(),
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
    given_any_petisco,
    make_user_created_event,
    given_random_organization,
    given_random_service,
    given_random_topic,
):
    event_before_delete_letter_stop = make_user_created_event("user_id_1")
    event_after_delete_letter_stop_1 = make_user_created_event(
        "user_id_after_delete_letter_stop_1"
    )
    event_after_delete_letter_stop_2 = make_user_created_event(
        "user_id_after_delete_letter_stop_2"
    )
    event_after_delete_letter_stop_3 = make_user_created_event(
        "user_id_after_delete_letter_stop_3"
    )

    filename_main_handler = "filename_main_handler.txt"
    filename_main_handler_requeue = "filename_main_handler_requeue.txt"

    if os.path.exists(filename_main_handler):
        os.remove(filename_main_handler)

    if os.path.exists(filename_main_handler_requeue):
        os.remove(filename_main_handler_requeue)

    @subscriber_handler()
    def main_handler(event: Event):
        print(f"main_handler: {event.to_json()}")
        with open(filename_main_handler, "a+") as fm:
            fm.write(event.to_json() + "\n")
        return isSuccess

    @subscriber_handler()
    def main_handler_requeue(event: Event):
        print(f"main_handler_requeue: {event.to_json()}")
        with open(filename_main_handler_requeue, "a+") as fp:
            fp.write(event.to_json() + "\n")
        return isSuccess

    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMqConnector(),
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
        connector=RabbitMqConnector(),
        subscribers={
            "dl-auth": ConfigEventSubscriber(
                organization=given_random_organization,
                service=given_random_service,
                topic=given_random_topic,
                handler=main_handler_requeue,
                dead_letter=True,
            )
        },
        connection_name="dl-subscriber",
    )

    publisher = RabbitMQEventPublisher(
        connector=RabbitMqConnector(),
        organization=given_random_organization,
        service=given_random_service,
        topic=given_random_topic,
    )

    subscriber.start()
    dl_subscriber.start()

    await_for_it(1.5)

    publisher.publish(event_before_delete_letter_stop)

    await_for_it(1.5)

    dl_subscriber.stop()

    await_for_it(5.5)

    publisher.publish_events(
        [
            event_after_delete_letter_stop_1,
            event_after_delete_letter_stop_2,
            event_after_delete_letter_stop_3,
        ]
    )

    await_for_it(1.5)

    with open(filename_main_handler, "r") as fmm:
        lines = fmm.readlines()
        events = []
        for line in lines:
            events.append(Event.from_json(line))

        assert event_before_delete_letter_stop == events[0]
        assert event_after_delete_letter_stop_1 == events[1]
        assert event_after_delete_letter_stop_2 == events[2]
        assert event_after_delete_letter_stop_3 == events[3]

    assert not os.path.exists(filename_main_handler_requeue)
    os.remove(filename_main_handler)

    subscriber.stop()
