from time import sleep

import pytest
from meiga import isSuccess, isFailure
from pika import ConnectionParameters, BlockingConnection

from petisco import (
    Event,
    subscriber_handler,
    RabbitMQEventPublisher,
    RabbitMQEventSubscriber,
    ConfigEventSubscriber,
)

from petisco.events.rabbitmq.rabbitmq_is_running_locally import (
    rabbitmq_is_running_locally,
)


def await_for_events():
    sleep(1.5)


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_work_successfully_a_happy_path_pub_sub(make_user_created_event):
    event = make_user_created_event()
    global received_events
    received_events = []

    @subscriber_handler()
    def main_handler(event: Event):
        global received_events
        received_events.append(event)

        if isinstance(event, make_user_created_event().__class__):
            assert event.user_id == "user_id_1"
            return isSuccess
        else:
            return isFailure

    connection = BlockingConnection(ConnectionParameters(host="localhost"))

    publisher = RabbitMQEventPublisher(
        connection=connection,
        organization="acme",
        service="pubsub",
        topic="pubsub-events",
    )

    publisher.publish_events([event, event])

    subscriber = RabbitMQEventSubscriber(
        connection=connection,
        subscribers={
            "auth": ConfigEventSubscriber(
                organization="acme",
                service="pubsub",
                topic="pubsub-events",
                handler=main_handler,
            )
        },
    )
    subscriber.subscribe_all()

    await_for_events()

    subscriber.unsubscribe_all()

    assert len(received_events) >= 2


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_publish_reject_and_requeue_from_dead_letter_exchange(
    make_user_created_event
):
    event = make_user_created_event()
    global received_events
    received_events = []
    global requeue_events
    requeue_events = []

    connection = BlockingConnection(ConnectionParameters(host="localhost"))
    publisher = RabbitMQEventPublisher(
        connection=connection,
        organization="acme",
        service="pubsub",
        topic="pubsub-events",
    )

    @subscriber_handler()
    def main_handler(event: Event):
        global received_events
        received_events.append(event)
        return isFailure

    @subscriber_handler()
    def requeue_from_dead_letter(event: Event):
        global requeue_events
        requeue_events.append(event)
        publisher.publish(event)
        return isFailure

    publisher.publish(event)

    subscriber = RabbitMQEventSubscriber(
        connection=connection,
        subscribers={
            "auth": ConfigEventSubscriber(
                organization="acme",
                service="pubsub",
                topic="pubsub-events",
                handler=main_handler,
            ),
            "dead-letter": ConfigEventSubscriber(
                organization="acme",
                service="pubsub",
                topic="pubsub-events",
                handler=requeue_from_dead_letter,
                dead_letter=True,
            ),
        },
    )
    subscriber.subscribe_all()

    await_for_events()

    subscriber.unsubscribe_all()

    assert len(received_events) >= 2
    assert len(requeue_events) >= 1
