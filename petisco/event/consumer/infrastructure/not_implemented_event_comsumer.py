from typing import Callable, List

from petisco.event.shared.domain.event_subscriber import EventSubscriber
from petisco.event.consumer.domain.interface_event_consumer import IEventConsumer


class NotImplementedEventConsumer(IEventConsumer):
    def start(self):
        pass

    def add_subscribers(self, subscribers: List[EventSubscriber]):
        pass

    def add_subscriber_on_dead_letter(
        self, subscriber: EventSubscriber, handler: Callable
    ):
        pass

    def add_handler_on_store(self, handler: Callable):
        pass

    def add_handler_on_queue(self, queue_name: str, handler: Callable):
        pass

    def unsubscribe_handler_on_queue(self, queue_name: str):
        pass

    def resume_handler_on_queue(self, queue_name: str):
        pass

    def stop(self):
        pass
