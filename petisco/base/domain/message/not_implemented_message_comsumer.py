from typing import Callable, List

from petisco import MessageConsumer, MessageSubscriber


class NotImplementedMessageConsumer(MessageConsumer):
    def start(self):
        pass

    def add_subscribers(self, subscribers: List[MessageSubscriber]):
        pass

    def add_subscriber_on_dead_letter(
        self, subscriber: MessageSubscriber, handler: Callable
    ):
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
