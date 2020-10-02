#!/usr/bin/env python
from meiga import isSuccess

from petisco import (
    Event,
    RabbitMQEventSubscriber,
    RabbitMQEventPublisher,
    ConfigEventSubscriber,
    subscriber_handler,
    RabbitMqConnector,
)

a_publisher = RabbitMQEventPublisher(
    connector=RabbitMqConnector(), organization="acme", service="a", topic=f"a-events"
)

b_publisher = RabbitMQEventPublisher(
    connector=RabbitMqConnector(), organization="acme", service="b", topic=f"b-events"
)


@subscriber_handler()
def a_requeue(event: Event):
    print(f"requeue > {event}")
    a_publisher.publish(event)
    return isSuccess


@subscriber_handler(delay_after=1)
def b_requeue(event: Event):
    print(f"requeue > {event}")
    b_publisher.publish(event)
    return isSuccess


subscriber = RabbitMQEventSubscriber(
    connector=RabbitMqConnector(),
    subscribers={
        "dl-a": ConfigEventSubscriber(
            organization="acme",
            service="a",
            topic="a-events",
            handler=a_requeue,
            dead_letter=True,
        ),
        "dl-b": ConfigEventSubscriber(
            organization="acme",
            service="b",
            topic="b-events",
            handler=b_requeue,
            dead_letter=True,
        ),
    },
    connection_name="petisco-subscribers",
)
subscriber.start()
