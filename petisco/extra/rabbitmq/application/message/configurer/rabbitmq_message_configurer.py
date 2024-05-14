from typing import List, Type, Union

from petisco.base.domain.message.message_configurer import MessageConfigurer
from petisco.base.domain.message.message_subscriber import MessageSubscriber
from petisco.extra.rabbitmq.application.message.configurer.rabbitmq_message_store_configurer import (
    RabbitMqMessageStoreConfigurer,
)
from petisco.extra.rabbitmq.application.message.configurer.rabbitmq_message_subscribers_configurer import (
    RabbitMqMessageSubcribersConfigurer,
)
from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_consumer_connector import (
    RabbitMqConsumerConnector,
)
from petisco.extra.rabbitmq.shared.queue_config import QueueConfig
from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector


class RabbitMqMessageConfigurer(MessageConfigurer):
    """
    A class to configure RabbitMQ infrastructure.
    This class configures exchanges, queue bindings and routing keys from defined MessageSubscribers.
    """

    def __init__(
        self,
        organization: str,
        service: str,
        connector: Union[RabbitMqConnector, RabbitMqConsumerConnector] = RabbitMqConnector(),
        queue_config: QueueConfig = QueueConfig.default(),
        use_store_queues: bool = True,
    ) -> None:
        self._use_store_queues = use_store_queues
        self.subscribers_configurer = RabbitMqMessageSubcribersConfigurer(
            organization, service, connector, queue_config
        )
        self.store_configurer = RabbitMqMessageStoreConfigurer(organization, service, connector, queue_config)

    def configure(self) -> None:
        """
        Define exchanges, queue bindings and routing key with empty subscribers.
        """
        self.configure_subscribers([])

    def configure_subscribers(
        self,
        subscribers: List[Type[MessageSubscriber]],
        clear_subscriber_before: bool = False,
        clear_store_before: bool = False,
    ) -> None:
        """
        Define exchanges, queue bindings and routing keys from given subscribers.
        """
        if subscribers is None:
            subscribers = []

        if clear_subscriber_before:
            self.subscribers_configurer.clear_subscribers(subscribers)
        if clear_store_before and self._use_store_queues:
            self.store_configurer.clear()

        self.subscribers_configurer.execute(subscribers)
        if self._use_store_queues:
            self.store_configurer.execute()

    def clear_subscribers(self, subscribers: List[MessageSubscriber]) -> None:
        """
        Clear configured subscribers.
        """
        if subscribers is None:
            subscribers = []

        self.subscribers_configurer.clear_subscribers(subscribers)
        if self._use_store_queues:
            self.store_configurer.clear()

    def clear(self) -> None:
        """
        Clear all configured subscribers and store configuration.
        """
        self.subscribers_configurer.clear()
        if self._use_store_queues:
            self.store_configurer.clear()
