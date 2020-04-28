#!/usr/bin/env python
import pika
from meiga import isSuccess

from petisco import (
    Event,
    RabbitMQEventSubscriber,
    RabbitMQEventPublisher,
    ConfigEventSubscriber,
    subscriber_handler,
)

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
publisher = RabbitMQEventPublisher(
    connection=connection,
    organization="acme",
    service="dashboard",
    topic=f"dashboard-events",
)


@subscriber_handler(delay_after=1)
def dashboard_handler(event: Event):
    publisher.publish(event)
    return isSuccess


subscriber = RabbitMQEventSubscriber(
    connection=connection,
    subscribers={
        "dl-dashboard": ConfigEventSubscriber(
            organization="acme",
            service="dashboard",
            topic="dashboard-events",
            handler=dashboard_handler,
            dead_letter=True,
        )
    },
)
