#!/usr/bin/env python
from meiga import isSuccess

from petisco import (
    subscriber_handler,
    RabbitMQEventSubscriber,
    ConfigEventSubscriber,
    Event,
    RabbitMqConnector,
)


@subscriber_handler()
def a_handler(event: Event):
    print(f" [x] a_handler {event}")
    return isSuccess


@subscriber_handler(percentage_simulate_nack=0.5)
def b_handler(event: Event):
    print(f" [x] b_handler {event}")
    return isSuccess


subscriber = RabbitMQEventSubscriber(
    connector=RabbitMqConnector(),
    subscribers={
        "a": ConfigEventSubscriber(
            organization="acme", service="a", topic="a-events", handler=a_handler
        ),
        "b": ConfigEventSubscriber(
            organization="acme", service="b", topic="b-events", handler=b_handler
        ),
    },
    connection_name="petisco-subscribers",
)
subscriber.start()
