from typing import List

from petisco.event.configurer.infrastructure.rabbitmq_event_store_configurer import (
    RabbitMqEventStoreConfigurer,
)
from petisco.event.configurer.infrastructure.rabbitmq_event_subscribers_configurer import (
    RabbitMqEventSubcribersConfigurer,
)
from petisco.event.queue.domain.queue_config import QueueConfig
from petisco.event.shared.domain.event import Event
from petisco.event.shared.domain.event_subscriber import EventSubscriber
from petisco.event.configurer.domain.interface_event_configurer import IEventConfigurer
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_connector import (
    RabbitMqConnector,
)


class RabbitMqEventConfigurer(IEventConfigurer):
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
        if subscribers is None:
            subscribers = []

        self.event_subscribers_configurer.execute(subscribers)
        if self._use_store_queues:
            self.event_store_configurer.execute()

    def clear(self):
        self.event_subscribers_configurer.clear()
        if self._use_store_queues:
            self.event_store_configurer.clear()
