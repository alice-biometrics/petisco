from typing import Callable, List, Type

from petisco.base.domain.message.message_consumer import MessageConsumer
from petisco.base.domain.message.message_subscriber import MessageSubscriber


class NotImplementedMessageConsumer(MessageConsumer):
    def start(self):
        pass

    def add_subscribers(self, subscribers: List[MessageSubscriber]):
        pass

    def add_subscriber_on_dead_letter(self, subscriber: Type[MessageSubscriber]):
        pass

    def add_handler_on_store(self, handler: Callable):
        pass

    def add_subscriber_on_queue(self, queue_name: str, handler: Callable):
        pass

    def unsubscribe_subscriber_on_queue(self, queue_name: str):
        pass

    def resume_subscriber_on_queue(self, queue_name: str):
        pass

    def stop(self):
        pass
