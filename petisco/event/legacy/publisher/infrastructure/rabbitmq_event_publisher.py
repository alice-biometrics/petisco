from typing import Dict

from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import StreamLostError
from pika import BasicProperties

from petisco.event.shared.domain.event import Event
from petisco.event.legacy.publisher.domain.interface_event_publisher import (
    IEventPublisher,
)

from petisco.event.legacy.rabbitmq.create_exchange_and_bind_queue import (
    create_exchange_and_bind_queue,
    create_dead_letter_exchange_and_bind_queue,
)
from petisco.event.legacy.rabbitmq.get_event_binding_key import get_event_binding_key
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_connector import (
    RabbitMqConnector,
)


class RabbitMQEventPublisher(IEventPublisher):
    def __init__(
        self, connector: RabbitMqConnector, organization: str, service: str, topic: str
    ):
        self.connector = connector
        self.organization = organization
        self.exchange = service
        self.queue = topic
        self.binding_key = get_event_binding_key(organization, service)
        self.properties = self._get_message_persistent_properties()
        self._connect()
        channel = self._get_channel()
        self._setup_exchanges_and_queues(channel)
        super().__init__()

    def _connect(self):
        if not self.connector:
            raise TypeError(f"RabbitMQEventPublisher: Invalid Given RabbitMQConnector")
        self.connection = self.connector.get_connection(
            f"{self.organization}.{self.exchange}"
        )

    def _setup_exchanges_and_queues(self, channel: BlockingChannel):
        create_dead_letter_exchange_and_bind_queue(
            channel=channel,
            exchange=self.exchange,
            queue=self.queue,
            binding_key=self.binding_key,
        )
        create_exchange_and_bind_queue(
            channel=channel,
            exchange=self.exchange,
            queue=self.queue,
            binding_key=self.binding_key,
            dead_letter=True,
        )

    def _get_event_routing_key(self, event: Event):
        """
        acme.onboarding.1.event.user.created
          |       |     |        |      |-> action (past verb)
          |       |     |        |-> domain entity
          |       |     |-> version
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
        if self.connection.is_open:
            self.connection.close()

    def _check_connection(self):
        if not self.connection.is_open:
            self._connect()

    def _get_channel(self) -> BlockingChannel:
        self._check_connection()
        try:
            channel = self.connection.channel()
        except StreamLostError:
            self._check_connection()
            channel = self.connection.channel()
        return channel

    def publish(self, event: Event):

        if not event:
            return

        channel = self._get_channel()

        routing_key = self._get_event_routing_key(event)

        channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=event.to_json(),
            properties=self.properties,
        )

        channel.close()
