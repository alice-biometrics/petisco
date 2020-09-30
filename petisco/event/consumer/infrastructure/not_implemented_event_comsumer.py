from typing import Callable, List

from petisco.event.shared.domain.event_subscriber import EventSubscriber
from petisco.event.consumer.domain.interface_event_consumer import IEventConsumer


class NotImplementedEventConsumer(IEventConsumer):
    def start(self):
        pass

    def consume_subscribers(self, subscribers: List[EventSubscriber]):
        pass

    def consume_dead_letter(self, subscriber: EventSubscriber, handler: Callable):
        pass

    def consume_store(self, handler: Callable):
        pass

    def consume_queue(self, queue_name: str, handler: Callable):
        pass

    def stop(self):
        pass
