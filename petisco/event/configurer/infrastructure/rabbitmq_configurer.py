from typing import List

from petisco.event.shared.domain.event import Event
from petisco.event.shared.domain.event_subscriber import EventSubscriber
from petisco.event.configurer.domain.interface_event_configurer import IEventConfigurer
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_exchange_name_formatter import (
    RabbitMqExchangeNameFormatter,
)
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_event_subscriber_queue_name_formatter import (
    RabbitMqEventSubscriberQueueNameFormatter,
)
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_connector import (
    RabbitMqConnector,
)


class RabbitMqEventConfigurer(IEventConfigurer):
    def __init__(
        self,
        connector: RabbitMqConnector,
        organization: str,
        service: str,
        use_store_queues: bool = True,
        retry_ttl: int = 5000,
    ):
        self._connector = connector
        self._exchange_name = f"{organization}.{service}"
        self._use_store_queues = use_store_queues
        self._configured_subscribers = []
        self.retry_ttl = retry_ttl

    def configure(self):
        self.configure_subscribers([])

    def configure_event(self, event: Event):
        self.configure_subscribers(
            [
                EventSubscriber(
                    event_name=event.event_name,
                    event_version=event.event_version,
                    handlers=[],
                )
            ]
        )

    def configure_subscribers(self, subscribers: List[EventSubscriber]):
        self._configure_exchanges()
        self._declare_queues(
            self._exchange_name,
            self._retry_exchange_name,
            self._dead_letter_exchange_name,
            subscribers,
        )
        self._configured_subscribers.append(subscribers)

    def clear(self):
        self._delete_exchange()
        self._delete_queues()

    def _delete_exchange(self):
        channel = self._connector.get_channel(self._exchange_name)
        channel.exchange_delete(self._exchange_name)
        channel.exchange_delete(self._retry_exchange_name)
        channel.exchange_delete(self._dead_letter_exchange_name)

    def _delete_queues(self):
        channel = self._connector.get_channel(self._exchange_name)
        channel.queue_delete("store")
        channel.queue_delete("retry.store")
        channel.queue_delete("dead_letter.store")
        for subscribers in self._configured_subscribers:
            for subscriber in subscribers:
                queue_name = RabbitMqEventSubscriberQueueNameFormatter.format(
                    subscriber, exchange_name=self._exchange_name
                )
                retry_queue_name = RabbitMqEventSubscriberQueueNameFormatter.format_retry(
                    subscriber, exchange_name=self._exchange_name
                )
                dead_letter_queue_name = RabbitMqEventSubscriberQueueNameFormatter.format_dead_letter(
                    subscriber, exchange_name=self._exchange_name
                )
                for suffix in subscriber.get_handlers_names():
                    name = f"{queue_name}.{suffix}"
                    retry_name = f"{retry_queue_name}.{suffix}"
                    dead_letter_name = f"{dead_letter_queue_name}.{suffix}"
                    channel.queue_delete(name)
                    channel.queue_delete(retry_name)
                    channel.queue_delete(dead_letter_name)

    def _configure_exchanges(self):
        self._retry_exchange_name = RabbitMqExchangeNameFormatter.retry(
            self._exchange_name
        )
        self._dead_letter_exchange_name = RabbitMqExchangeNameFormatter.dead_letter(
            self._exchange_name
        )
        self._declare_exchange(self._exchange_name)
        self._declare_exchange(self._retry_exchange_name)
        self._declare_exchange(self._dead_letter_exchange_name)

    def _declare_exchange(self, exchange_name: str):
        channel = self._connector.get_channel(self._exchange_name)
        try:
            channel.exchange_declare(
                exchange=exchange_name, exchange_type="topic", durable=True
            )
        except Exception as error:
            raise TypeError(
                f"RabbitMQEventPublisher: Cannot create the exchange ({exchange_name})\n{error}"
            )

    def _declare_queues(
        self,
        exchange_name: str,
        retry_exchange_name: str,
        dead_letter_exchange_name: str,
        subscribers: List[EventSubscriber],
    ):
        if self._use_store_queues:
            self._declare_store_queues(
                exchange_name, retry_exchange_name, dead_letter_exchange_name
            )

        for subscriber in subscribers:
            base_queue_name = RabbitMqEventSubscriberQueueNameFormatter.format(
                subscriber, exchange_name=exchange_name
            )
            base_retry_queue_name = RabbitMqEventSubscriberQueueNameFormatter.format_retry(
                subscriber, exchange_name=exchange_name
            )
            base_dead_letter_queue_name = RabbitMqEventSubscriberQueueNameFormatter.format_dead_letter(
                subscriber, exchange_name=exchange_name
            )
            routing_key = base_queue_name

            for suffix in subscriber.get_handlers_names():
                queue_name = f"{base_queue_name}.{suffix}"
                retry_queue_name = f"{base_retry_queue_name}.{suffix}"
                dead_letter_queue_name = f"{base_dead_letter_queue_name}.{suffix}"

                self._declare_queue(queue_name=queue_name)
                self._declare_queue(
                    queue_name=retry_queue_name,
                    dead_letter_exchange=exchange_name,
                    dead_letter_routing_key=f"retry.{queue_name}",
                    message_ttl=self.retry_ttl,
                )
                self._declare_queue(queue_name=dead_letter_queue_name)

                self._bind_queue(
                    exchange_name=exchange_name,
                    queue_name=queue_name,
                    routing_key=routing_key,
                )
                self._bind_queue(
                    exchange_name=exchange_name,
                    queue_name=queue_name,
                    routing_key=f"retry.{queue_name}",
                )
                self._bind_queue(
                    exchange_name=retry_exchange_name,
                    queue_name=retry_queue_name,
                    routing_key=f"retry.{queue_name}",
                )
                self._bind_queue(
                    exchange_name=dead_letter_exchange_name,
                    queue_name=dead_letter_queue_name,
                    routing_key=f"dead_letter.{queue_name}",
                )

    def _declare_store_queues(
        self,
        exchange_name: str,
        retry_exchange_name: str,
        dead_letter_exchange_name: str,
    ):
        self._declare_queue(queue_name="store")
        self._declare_queue(
            queue_name="retry.store",
            dead_letter_exchange=exchange_name,
            dead_letter_routing_key="retry.store",
            message_ttl=self.retry_ttl,
        )
        self._declare_queue(queue_name="dead_letter.store")

        routing_key_any_event = f"*.*.*.event.*"
        self._bind_queue(
            exchange_name=exchange_name,
            queue_name="store",
            routing_key=routing_key_any_event,
        )
        self._bind_queue(
            exchange_name=exchange_name, queue_name="store", routing_key="retry.store"
        )
        self._bind_queue(
            exchange_name=retry_exchange_name,
            queue_name="retry.store",
            routing_key="retry.store",
        )
        self._bind_queue(
            exchange_name=retry_exchange_name,
            queue_name="retry.store",
            routing_key=f"retry.store",
        )
        self._bind_queue(
            exchange_name=dead_letter_exchange_name,
            queue_name="dead_letter.store",
            routing_key=f"dead_letter.{routing_key_any_event}",
        )

    def _declare_queue(
        self,
        queue_name: str,
        dead_letter_exchange: str = None,
        dead_letter_routing_key: str = None,
        message_ttl: int = None,
    ):
        channel = self._connector.get_channel(self._exchange_name)

        queue_arguments = {}
        if dead_letter_exchange:
            queue_arguments["x-dead-letter-exchange"] = dead_letter_exchange

        if dead_letter_routing_key:
            queue_arguments["x-dead-letter-routing-key"] = dead_letter_routing_key

        if message_ttl:
            queue_arguments["x-message-ttl"] = message_ttl

        result = channel.queue_declare(
            queue=queue_name, arguments=queue_arguments, durable=True
        )

        return result.method.queue

    def _bind_queue(self, exchange_name: str, queue_name: str, routing_key: str):
        channel = self._connector.get_channel(self._exchange_name)

        channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key=routing_key
        )
