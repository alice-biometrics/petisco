from pika import BasicProperties
from pika.exceptions import ChannelClosedByBroker

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.domain_event_bus import DomainEventBus
from petisco.extra.rabbitmq.application.message.rabbitmq_domain_event_configurer import (
    RabbitMqDomainEventConfigurer,
)
from petisco.extra.rabbitmq.application.message.rabbitmq_domain_event_queue_name_formatter import (
    RabbitMqDomainEventQueueNameFormatter,
)
from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector


class RabbitMqDomainEventBus(DomainEventBus):
    def __init__(self, connector: RabbitMqConnector, organization: str, service: str):
        self.connector = connector
        self.exchange_name = f"{organization}.{service}"
        self.rabbitmq_key = f"publisher-{self.exchange_name}"
        self.configurer = RabbitMqDomainEventConfigurer(
            connector, organization, service
        )
        self.properties = BasicProperties(delivery_mode=2)  # PERSISTENT_TEXT_PLAIN

    def publish(self, domain_event: DomainEvent):
        self._check_is_domain_event(domain_event)
        meta = self.get_configured_meta()
        domain_event = domain_event.update_meta(meta)

        try:
            channel = self.connector.get_channel(self.rabbitmq_key)
            routing_key = RabbitMqDomainEventQueueNameFormatter.format(
                domain_event, exchange_name=self.exchange_name
            )

            channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=domain_event.json(),
                properties=self.properties,
            )
        except ChannelClosedByBroker:
            # If Event queue is not configured, it will be configured and publication retried.
            self.configurer.configure_event(domain_event)
            self.publish(domain_event)

    def retry_publish_only_on_store_queue(self, domain_event: DomainEvent):
        self._check_is_domain_event(domain_event)
        meta = self.get_configured_meta()
        domain_event = domain_event.update_meta(meta)

        channel = self.connector.get_channel(self.rabbitmq_key)
        channel.basic_publish(
            exchange=self.exchange_name,
            routing_key="retry.store",
            body=domain_event.json(),
            properties=self.properties,
        )

    def close(self):
        self.connector.close(self.rabbitmq_key)
