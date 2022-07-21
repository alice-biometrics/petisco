from typing import List, Union

from pika import BasicProperties
from pika.exceptions import ChannelClosedByBroker

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.domain_event_bus import DomainEventBus
from petisco.extra.rabbitmq.application.message.configurer.rabbitmq_message_configurer import (
    RabbitMqMessageConfigurer,
)
from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_consumer_connector import (
    RabbitMqConsumerConnector,
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
        connector: Union[
            RabbitMqConnector, RabbitMqConsumerConnector
        ] = RabbitMqConnector(),
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
            if channel.is_open and not isinstance(
                self.connector, RabbitMqConsumerConnector
            ):
                channel.close()

        except ChannelClosedByBroker:
            self._retry(domain_event)

    def publish_list(self, domain_events: List[DomainEvent]):
        meta = self.get_configured_meta()
        unpublished_domain_events = domain_events
        try:
            channel = self.connector.get_channel(self.rabbitmq_key)

            for i, domain_event in enumerate(domain_events):
                self._check_is_domain_event(domain_event)
                domain_event = domain_event.update_meta(meta)
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
                unpublished_domain_events.pop(i)
            if channel.is_open and not isinstance(
                self.connector, RabbitMqConsumerConnector
            ):
                channel.close()
        except ChannelClosedByBroker:
            self._retry_publish_list(unpublished_domain_events)

    def _retry(self, domain_event: DomainEvent):
        # If domain event queue is not configured, it will be configured and then try to publish again.
        self.configurer.configure()
        self.publish(domain_event)

    def _retry_publish_list(self, domain_events: List[DomainEvent]):
        # If domain event queue is not configured, it will be configured and then try to publish again.
        self.configurer.configure()
        self.publish_list(domain_events)

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

    def retry_publish(
        self,
        domain_event: DomainEvent,
        retry_routing_key: str,
        retry_exchange_name: str = None,
    ):
        self._check_is_domain_event(domain_event)
        meta = self.get_configured_meta()
        domain_event = domain_event.update_meta(meta)
        try:
            channel = self.connector.get_channel(self.rabbitmq_key)
            channel.confirm_delivery()

            retry_exchange = (
                retry_exchange_name
                if retry_exchange_name
                else f"retry.{self.exchange_name}"
            )

            channel.basic_publish(
                exchange=retry_exchange,
                routing_key=retry_routing_key,
                body=domain_event.json(),
                properties=self.properties,
            )
        except ChannelClosedByBroker:
            self._retry(domain_event)

    def close(self):
        self.connector.close(self.rabbitmq_key)
