from typing import List, Type

from petisco.base.domain.message.message_subscriber import MessageSubscriber
from petisco.extra.rabbitmq.application.message.formatter.rabbitmq_message_subscriber_queue_name_formatter import (
    RabbitMqMessageSubscriberQueueNameFormatter,
)
from petisco.extra.rabbitmq.shared.queue_config import QueueConfig
from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector
from petisco.extra.rabbitmq.shared.rabbitmq_declarer import RabbitMqDeclarer
from petisco.extra.rabbitmq.shared.rabbitmq_exchange_name_formatter import (
    RabbitMqExchangeNameFormatter,
)


class RabbitMqMessageSubcribersConfigurer:
    def __init__(
        self,
        organization: str,
        service: str,
        connector: RabbitMqConnector,
        queue_config: QueueConfig,
    ):
        self._connector = connector
        self._exchange_name = f"{organization}.{service}"
        self._retry_exchange_name = RabbitMqExchangeNameFormatter.retry(
            self._exchange_name
        )
        self._dead_letter_exchange_name = RabbitMqExchangeNameFormatter.dead_letter(
            self._exchange_name
        )
        self.rabbitmq = RabbitMqDeclarer(
            connector=self._connector, channel_name=self._exchange_name
        )
        self._configured_subscribers = []
        self.queue_config = queue_config

    def execute(self, subscribers):
        self._configure_exchanges()
        self._declare_queues(
            self._exchange_name,
            self._retry_exchange_name,
            self._dead_letter_exchange_name,
            subscribers,
        )
        self._configured_subscribers += subscribers

    def clear(self):
        self._delete_exchange()
        self._delete_queues()

    def _configure_exchanges(self):
        self.rabbitmq.declare_exchange(self._exchange_name)
        self.rabbitmq.declare_exchange(self._retry_exchange_name)
        self.rabbitmq.declare_exchange(self._dead_letter_exchange_name)

    def _delete_exchange(self):
        self.rabbitmq.delete_exchange(self._exchange_name)
        self.rabbitmq.delete_exchange(self._retry_exchange_name)
        self.rabbitmq.delete_exchange(self._dead_letter_exchange_name)

    def _delete_queues(self):
        for SubscriberClass in self._configured_subscribers:

            subscriber = SubscriberClass()
            for subscriber_info in subscriber.get_message_subscribers_info():

                if subscriber_info.message_type == "message":
                    # if subscriber_info is subscribed to message it will be consuming from store queue
                    break

                queue_name = RabbitMqMessageSubscriberQueueNameFormatter.format(
                    subscriber_info, exchange_name=self._exchange_name
                )
                retry_queue_name = (
                    RabbitMqMessageSubscriberQueueNameFormatter.format_retry(
                        subscriber_info, exchange_name=self._exchange_name
                    )
                )
                dead_letter_queue_name = (
                    RabbitMqMessageSubscriberQueueNameFormatter.format_dead_letter(
                        subscriber_info, exchange_name=self._exchange_name
                    )
                )

                suffix = subscriber.get_subscriber_name()
                name = f"{queue_name}.{suffix}"
                retry_name = f"{retry_queue_name}.{suffix}"
                dead_letter_name = f"{dead_letter_queue_name}.{suffix}"
                self.rabbitmq.delete_queue(name)
                self.rabbitmq.delete_queue(retry_name)
                self.rabbitmq.delete_queue(dead_letter_name)

    def _declare_queues(
        self,
        exchange_name: str,
        retry_exchange_name: str,
        dead_letter_exchange_name: str,
        subscribers: List[Type[MessageSubscriber]],
    ):

        for SubscriberClass in subscribers:
            subscriber = SubscriberClass()
            for subscriber_info in subscriber.get_message_subscribers_info():

                if subscriber_info.message_type == "message":
                    # if subscriber_info is subscribed to message it will be consuming from store queue
                    break

                base_queue_name = RabbitMqMessageSubscriberQueueNameFormatter.format(
                    subscriber_info, exchange_name=exchange_name
                )
                base_retry_queue_name = (
                    RabbitMqMessageSubscriberQueueNameFormatter.format_retry(
                        subscriber_info, exchange_name=exchange_name
                    )
                )
                base_dead_letter_queue_name = (
                    RabbitMqMessageSubscriberQueueNameFormatter.format_dead_letter(
                        subscriber_info, exchange_name=exchange_name
                    )
                )
                routing_key = base_queue_name
                suffix = subscriber.get_subscriber_name()

                queue_name = f"{base_queue_name}.{suffix}"
                retry_queue_name = f"{base_retry_queue_name}.{suffix}"
                dead_letter_queue_name = f"{base_dead_letter_queue_name}.{suffix}"

                main_ttl = self.queue_config.get_main_ttl(queue_name)
                retry_ttl = self.queue_config.get_retry_ttl(queue_name)

                self.rabbitmq.declare_queue(
                    queue_name=queue_name,
                    dead_letter_exchange=f"dead_letter.{exchange_name}",
                    dead_letter_routing_key="dead_letter",
                    message_ttl=main_ttl,
                )
                self.rabbitmq.declare_queue(
                    queue_name=retry_queue_name,
                    dead_letter_exchange=exchange_name,
                    dead_letter_routing_key=f"retry.{queue_name}",
                    message_ttl=retry_ttl,
                )
                self.rabbitmq.declare_queue(queue_name=dead_letter_queue_name)

                self.rabbitmq.bind_queue(
                    exchange_name=exchange_name,
                    queue_name=queue_name,
                    routing_key=routing_key,
                )
                self.rabbitmq.bind_queue(
                    exchange_name=exchange_name,
                    queue_name=queue_name,
                    routing_key=f"retry.{queue_name}",
                )
                self.rabbitmq.bind_queue(
                    exchange_name=retry_exchange_name,
                    queue_name=retry_queue_name,
                    routing_key=f"retry.{queue_name}",
                )
                self.rabbitmq.bind_queue(
                    exchange_name=dead_letter_exchange_name,
                    queue_name=dead_letter_queue_name,
                    routing_key=f"dead_letter.{queue_name}",
                )
                self.rabbitmq.bind_queue(
                    exchange_name=dead_letter_exchange_name,
                    queue_name=dead_letter_queue_name,
                    routing_key="dead_letter",
                )
