from typing import List

from petisco.base.domain.message.message import Message
from petisco.base.domain.message.message_configurer import MessageConfigurer
from petisco.base.domain.message.message_subscriber import MessageSubscriber
from petisco.extra.rabbitmq.application.message.configurer.rabbitmq_message_store_configurer import (
    RabbitMqMessageStoreConfigurer,
)
from petisco.extra.rabbitmq.application.message.configurer.rabbitmq_message_subscribers_configurer import (
    RabbitMqMessageSubcribersConfigurer,
)
from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector
from petisco.extra.rabbitmq.shared.queue_config import QueueConfig


class RabbitMqMessageConfigurer(MessageConfigurer):
    def __init__(
        self,
        connector: RabbitMqConnector,
        organization: str,
        service: str,
        queue_config: QueueConfig = QueueConfig.default(),
        use_store_queues: bool = True,
    ):
        self._use_store_queues = use_store_queues
        self.subscribers_configurer = RabbitMqMessageSubcribersConfigurer(
            connector, organization, service, queue_config
        )
        self.store_configurer = RabbitMqMessageStoreConfigurer(
            connector, organization, service, queue_config
        )

    def configure(self):
        self.configure_subscribers([])

    def configure_message(self, message: Message):
        self.configure_subscribers(
            [
                MessageSubscriber(
                    message_name=message.name,
                    message_version=message.version,
                    message_type=message.type,
                    handlers=[],
                )
            ]
        )

    def configure_subscribers(self, subscribers: List[MessageSubscriber]):
        if subscribers is None:
            subscribers = []

        self.subscribers_configurer.execute(subscribers)
        if self._use_store_queues:
            self.store_configurer.execute()

    def clear(self):
        self.subscribers_configurer.clear()
        if self._use_store_queues:
            self.store_configurer.clear()
