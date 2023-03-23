from typing import List, Union

from deprecation import deprecated
from pika.exceptions import ChannelClosedByBroker

from petisco import __version__
from petisco.base.application.chaos.check_chaos import check_chaos_publication
from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.domain_event_bus import DomainEventBus
from petisco.extra.rabbitmq.application.message.bus.rabbitmq_message_publisher import (
    RabbitMqMessagePublisher,
)
from petisco.extra.rabbitmq.application.message.configurer.rabbitmq_message_configurer import (
    RabbitMqMessageConfigurer,
)
from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_consumer_connector import (
    RabbitMqConsumerConnector,
)
from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector


class RabbitMqDomainEventBus(DomainEventBus):
    """
    An implementation of DomainEventBus using RabbitMQ infrastructure.
    Implementation is based on pika library.
    """

    def __init__(
        self,
        organization: str,
        service: str,
        connector: Union[
            RabbitMqConnector, RabbitMqConsumerConnector
        ] = RabbitMqConnector(),
        fallback: Union[DomainEventBus, None] = None,
    ):
        self.connector = connector
        self.exchange_name = f"{organization}.{service}"
        self.rabbitmq_key = f"publisher-{self.exchange_name}"
        self.configurer = RabbitMqMessageConfigurer(organization, service, connector)
        self.already_configured = False
        self.fallback = fallback
        self.publisher = RabbitMqMessagePublisher(self.exchange_name)

    def publish(self, domain_event: Union[DomainEvent, List[DomainEvent]]) -> None:
        """
        Publish a DomainEvent or a list of DomainEvents
        """

        meta = self.get_configured_meta()
        published_domain_event = []
        domain_events = self._check_input(domain_event)

        try:
            check_chaos_publication()
            channel = self.connector.get_channel(self.rabbitmq_key)
            for domain_event in domain_events:
                self._check_is_domain_event(domain_event)
                domain_event = domain_event.update_meta(meta)
                self.publisher.execute(channel, domain_event)
                published_domain_event.append(domain_event)
            if channel.is_open and not isinstance(
                self.connector, RabbitMqConsumerConnector
            ):
                channel.close()
        except ChannelClosedByBroker:
            unpublished_domain_events = [
                event for event in domain_events if event not in published_domain_event
            ]
            self._retry(unpublished_domain_events)
        except Exception as exc:  # noqa
            if not self.fallback:
                raise exc

            unpublished_domain_events = [
                event for event in domain_events if event not in published_domain_event
            ]
            self.fallback.publish(unpublished_domain_events)

    @deprecated(
        deprecated_in="1.14.0",
        removed_in="2.0.0",
        current_version=__version__,
        details="Use publish function instead",
    )
    def publish_list(self, domain_events: List[DomainEvent]) -> None:
        self.publish(domain_events)

    def _retry(self, domain_events: List[DomainEvent]) -> None:
        # If domain event queue is not configured, it will be configured and then try to publish again.
        if not self.already_configured:
            self.configurer.configure()
            self.already_configured = True
            self.publish(domain_events)
        elif self.fallback:
            self.fallback.publish(domain_events)

    @deprecated(
        deprecated_in="1.14.0",
        removed_in="2.0.0",
        current_version=__version__,
        details="Use publish function instead. If you want publish with different routing keys, implement new object",
    )
    def retry_publish_only_on_store_queue(self, domain_event: DomainEvent) -> None:
        self._check_is_domain_event(domain_event)
        meta = self.get_configured_meta()
        domain_event = domain_event.update_meta(meta)

        channel = self.connector.get_channel(self.rabbitmq_key)
        self.publisher.execute(channel, domain_event, routing_key="retry.store")

    def close(self) -> None:
        """
        Close RabbitMQ connection.
        """
        self.connector.close(self.rabbitmq_key)
