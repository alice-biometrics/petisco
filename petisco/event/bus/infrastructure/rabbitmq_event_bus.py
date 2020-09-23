from typing import Dict

from pika import BasicProperties
from pika.exceptions import ChannelClosedByBroker

from petisco.event.bus.domain.interface_event_bus import IEventBus
from petisco.event.configurer.infrastructure.rabbitmq_configurer import (
    RabbitMqEventConfigurer,
)
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_queue_name_formatter import (
    RabbitMqQueueNameFormatter,
)
from petisco.event.shared.domain.event import Event

from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_connector import (
    RabbitMqConnector,
)


class RabbitMqEventBus(IEventBus):
    def __init__(self, connector: RabbitMqConnector, organization: str, service: str):
        self.connector = connector
        self.exchange_name = f"{organization}.{service}"
        self.configurer = RabbitMqEventConfigurer(connector, organization, service)
        self.properties = BasicProperties(delivery_mode=2)  # PERSISTENT_TEXT_PLAIN

    def info(self) -> Dict:
        return {
            "name": self.__class__.__name__,
            "connection.is_open": self.connector.get_connection(
                self.exchange_name
            ).is_open,
        }

    def publish(self, event: Event):

        if not event or not issubclass(event.__class__, Event):
            raise TypeError("Bus only publishes petisco.Event objects")

        try:
            channel = self.connector.get_channel(self.exchange_name)

            routing_key = RabbitMqQueueNameFormatter.format(
                event, exchange_name=self.exchange_name
            )

            channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=event.to_json(),
                properties=self.properties,
            )

            channel.close()
        except ChannelClosedByBroker:
            # If Event queue is not configured, it will be configured and publication retried.
            self.configurer.configure_event(event)
            self.publish(event)

    def close(self):
        if self.connector.get_connection(self.exchange_name).is_open:
            self.connector.get_connection(self.exchange_name).close()
