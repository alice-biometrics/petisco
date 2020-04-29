from typing import Dict

from pika import BlockingConnection, BasicProperties

from petisco.events.event import Event
from petisco.events.publisher.domain.interface_event_publisher import IEventPublisher

from petisco.events.rabbitmq.create_exchange_and_bind_queue import (
    create_exchange_and_bind_queue,
    create_dead_letter_exchange_and_bind_queue,
)
from petisco.events.rabbitmq.get_event_binding_key import get_event_binding_key


class RabbitMQEventPublisher(IEventPublisher):
    def __init__(
        self,
        connection: BlockingConnection,
        organization: str,
        service: str,
        topic: str,
    ):
        if not connection:
            raise TypeError(
                f'RabbitMQEventPublisher: Invalid Given Connection. Please, check with something similar to BlockingConnection(ConnectionParameters(host="localhost"))'
            )

        self.connection = connection
        self.organization = organization
        self.exchange = service
        self.queue = topic
        self.binding_key = get_event_binding_key(organization, service)
        self.properties = self._get_message_persistent_properties()
        self._setup_exchanges_and_queues()
        super().__init__()

    def _setup_exchanges_and_queues(self):
        create_dead_letter_exchange_and_bind_queue(
            connection=self.connection,
            exchange=self.exchange,
            queue=self.queue,
            binding_key=self.binding_key,
        )
        create_exchange_and_bind_queue(
            connection=self.connection,
            exchange=self.exchange,
            queue=self.queue,
            binding_key=self.binding_key,
            dead_letter=True,
        )

    def _get_event_routing_key(self, event: Event):
        """
        acme.onboarding.1.event.user.created
          |       |      |        |      |-> Action (past verb)
          |       |      |        |-> domain entity
          |       |      |-> version
          |       |-> service
          |-> organization
        """
        return f"{self.organization}.{self.exchange}.{event.event_version}.event.{event.event_name}"

    def _get_message_persistent_properties(self):
        """
        Make message persistent (PERSISTENT_TEXT_PLAIN)
        """
        return BasicProperties(delivery_mode=2)

    def info(self) -> Dict:
        return {
            "name": self.__class__.__name__,
            "connection.is_open": self.connection.is_open,
        }

    def close(self):
        self.connection.close()

    def publish(self, event: Event):
        if not event:
            return

        channel = self.connection.channel()

        routing_key = self._get_event_routing_key(event)

        channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=event.to_json(),
            properties=self.properties,
        )

        channel.close()
