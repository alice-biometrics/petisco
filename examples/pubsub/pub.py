#!/usr/bin/env python
from time import sleep

import pika

from petisco import Event
from petisco.domain.value_objects.user_id import UserId
from petisco.events.publisher.infrastructure.rabbitmq_event_publisher import (
    RabbitMQEventPublisher,
)


class UserCreated(Event):
    user_id: UserId

    def __init__(self, user_id: UserId):
        self.user_id = user_id
        self.event_version = "1"
        super().__init__()


connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
publishers = {}
for service in ["auth", "dashboard"]:
    publisher = RabbitMQEventPublisher(
        connection=connection,
        organization="acme",
        service=service,
        topic=f"{service}-events",
    )
    publishers[service] = publisher

for i in range(10):
    for name, publisher in publishers.items():
        event = UserCreated(UserId.generate())
        print(f"Publishing: {name} -> {event}")
        publisher.publish(event)
        sleep(1)
