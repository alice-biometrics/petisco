from time import sleep

import pytest
from pika import ConnectionParameters

from petisco import Event, RabbitMQEventManager, UserId
from petisco.events.rabbitmq.rabbitmq_is_running_locally import (
    rabbitmq_is_running_locally,
)


def await_for_events():
    sleep(1.5)


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_create_a_rabbitmq_event_manager_and_publish_two_different_events(
    make_user_created_event, make_first_name_added_event, given_any_topic
):
    given_rabbitmq_local_connection_parameters = ConnectionParameters(host="localhost")

    global received_events
    received_events = []

    def callback(ch, method, properties, body):
        event = Event.from_json(body)
        global received_events
        received_events.append(event)

        if isinstance(event, make_user_created_event().__class__):
            assert event.user_id == "user_id"

        elif isinstance(event, make_first_name_added_event().__class__):
            assert event.user_id == "user_id"
            assert event.first_name == "Any User"
        ch.basic_ack(delivery_tag=method.delivery_tag)

    event_manager = RabbitMQEventManager(
        connection_parameters=given_rabbitmq_local_connection_parameters,
        subscribers={given_any_topic: callback},
    )

    event_manager.send(given_any_topic, make_user_created_event())
    event_manager.send(given_any_topic, make_first_name_added_event())

    await_for_events()

    event_manager.unsubscribe_all()

    assert len(received_events) >= 2


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_unsubscribe_all_successfully(make_user_created_event):
    given_any_user_id_1 = UserId("user_id_1")
    given_any_user_id_2 = UserId("user_id_2")
    given_any_topic = "topic"

    def callback(ch, method, properties, body):
        event = Event.from_json(body)
        global received_events
        received_events.append(event)

        if isinstance(event, make_user_created_event().__class__):
            assert event.user_id == "user_id_1"
            ch.basic_ack(delivery_tag=method.delivery_tag)

    event_manager = RabbitMQEventManager(
        connection_parameters=ConnectionParameters(host="localhost"),
        subscribers={given_any_topic: callback},
    )

    event_manager.send(
        given_any_topic, make_user_created_event(user_id=given_any_user_id_1)
    )
    event_manager.unsubscribe_all()
    sleep(0.8)

    event_manager.send(
        given_any_topic, make_user_created_event(user_id=given_any_user_id_2)
    )

    await_for_events()

    assert len(received_events) >= 1
