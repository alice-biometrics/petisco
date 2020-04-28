#!/usr/bin/env python
import pika
from meiga import isSuccess

from petisco import (
    subscriber_handler,
    RabbitMQEventSubscriber,
    ConfigEventSubscriber,
    Event,
)


connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))


@subscriber_handler()
def auth_handler(event: Event):
    print(f" [x] auth_handler {event}")
    return isSuccess


@subscriber_handler(percentage_simulate_rejection=0.5)
def dashboard_handler(event: Event):
    print(f" [x] dashboard_handler {event}")
    return isSuccess


subscriber = RabbitMQEventSubscriber(
    connection=connection,
    subscribers={
        "auth": ConfigEventSubscriber(
            organization="acme",
            service="auth",
            topic="auth-events",
            handler=auth_handler,
        ),
        "dashboard": ConfigEventSubscriber(
            organization="acme",
            service="dashboard",
            topic="dashboard-events",
            handler=dashboard_handler,
        ),
    },
)
