from pika import BasicProperties
from pika.exceptions import ChannelClosedByBroker

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.domain_event_bus import DomainEventBus
from petisco.extra.rabbitmq.application.message.configurer.rabbitmq_message_configurer import (
    RabbitMqMessageConfigurer,
)
from petisco.extra.rabbitmq.application.message.formatter.rabbitmq_message_queue_name_formatter import (
    RabbitMqMessageQueueNameFormatter,
)
from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector


class RabbitMqDomainEventBus(DomainEventBus):
    def __init__(
        self,
        organization: str,
        service: str,
        connector: RabbitMqConnector = RabbitMqConnector(),
    ):
        self.connector = connector
        self.exchange_name = f"{organization}.{service}"
        self.rabbitmq_key = f"publisher-{self.exchange_name}"
        self.configurer = RabbitMqMessageConfigurer(organization, service, connector)
        self.properties = BasicProperties(delivery_mode=2)  # PERSISTENT_TEXT_PLAIN

    def publish(self, domain_event: DomainEvent):
        self._check_is_domain_event(domain_event)
        meta = self.get_configured_meta()
        domain_event = domain_event.update_meta(meta)
        try:
            channel = self.connector.get_channel(self.rabbitmq_key)
            routing_key = RabbitMqMessageQueueNameFormatter.format(
                domain_event, exchange_name=self.exchange_name
            )
            channel.confirm_delivery()
            channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=domain_event.json(),
                properties=self.properties,
            )
        except ChannelClosedByBroker:
            self._retry(domain_event)

    def _retry(self, domain_event: DomainEvent):
        # If domain event queue is not configured, it will be configured and then try to publish again.
        self.configurer.configure()
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
