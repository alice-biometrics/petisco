from typing import List

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.message_subscriber import MessageSubscriber
from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector
from petisco.legacy.event.configurer.domain.interface_event_configurer import (
    IEventConfigurer,
)
from petisco.legacy.event.configurer.infrastructure.rabbitmq_event_store_configurer import (
    RabbitMqEventStoreConfigurer,
)
from petisco.legacy.event.configurer.infrastructure.rabbitmq_event_subscribers_configurer import (
    RabbitMqEventSubcribersConfigurer,
)
from petisco.legacy.event.queue.domain.queue_config import QueueConfig


class RabbitMqDomainEventConfigurer(IEventConfigurer):
    def __init__(
        self,
        connector: RabbitMqConnector,
        organization: str,
        service: str,
        queue_config: QueueConfig = QueueConfig.default(),
        use_store_queues: bool = True,
    ):
        self._use_store_queues = use_store_queues
        self.event_subscribers_configurer = RabbitMqEventSubcribersConfigurer(
            connector, organization, service, queue_config
        )
        self.event_store_configurer = RabbitMqEventStoreConfigurer(
            connector, organization, service, queue_config
        )

    def configure(self):
        self.configure_subscribers([])

    def configure_event(self, domain_event: DomainEvent):
        self.configure_subscribers(
            [
                MessageSubscriber(
                    message_name=domain_event.name,
                    message_version=domain_event.version,
                    handlers=[],
                )
            ]
        )

    def configure_subscribers(self, subscribers: List[MessageSubscriber]):
        if subscribers is None:
            subscribers = []

        self.event_subscribers_configurer.execute(subscribers)
        if self._use_store_queues:
            self.event_store_configurer.execute()

    def clear(self):
        self.event_subscribers_configurer.clear()
        if self._use_store_queues:
            self.event_store_configurer.clear()
