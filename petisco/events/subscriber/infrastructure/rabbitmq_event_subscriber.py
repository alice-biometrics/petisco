import threading
from typing import Dict

from pika import BlockingConnection

from petisco.events.rabbitmq.create_exchange_and_bind_queue import (
    create_exchange_and_bind_queue,
    create_dead_letter_exchange_and_bind_queue,
)
from petisco.events.rabbitmq.get_event_binding_key import get_event_binding_key
from petisco.events.subscriber.domain.config_event_subscriber import (
    ConfigEventSubscriber,
)
from petisco.events.subscriber.domain.interface_event_subscriber import IEventSubscriber


class RabbitMQEventSubscriber(IEventSubscriber):
    def __init__(
        self,
        connection: BlockingConnection,
        subscribers: Dict[str, ConfigEventSubscriber] = None,
    ):
        if not connection:
            raise TypeError(
                f'RabbitMQEventSubscriber: Invalid Given Connection. Please, check with something similar to BlockingConnection(ConnectionParameters(host="localhost"))'
            )
        self.connection = connection
        self._is_subscribed = False
        super().__init__(subscribers)

    def subscribe_all(self):
        if self.subscribers:
            # Run the worker into a thread
            self._thread = threading.Thread(target=self._subscribe)
            self._thread.start()
            self._is_subscribed = True

    def _subscribe(self):
        self._channel = self.connection.channel()
        # This uses the basic.qos protocol method to tell RabbitMQ not to give more than one message to a worker at a
        # time. Or, in other words, don't dispatch a new message to a worker until it has processed and acknowledged
        # the previous one. Instead, it will dispatch it to the next worker that is not still busy.
        self._channel.basic_qos(prefetch_count=1)

        for name, subscriber_config in self.subscribers.items():
            self._setup_exchanges_and_queues(subscriber_config)
            queue = (
                subscriber_config.topic
                if not subscriber_config.dead_letter
                else f"dl-{subscriber_config.topic}"
            )
            self._channel.basic_consume(
                queue=queue, on_message_callback=subscriber_config.get_handler()
            )

        self._channel.start_consuming()

    def _setup_exchanges_and_queues(self, subscriber_config: ConfigEventSubscriber):
        exchange = subscriber_config.service
        queue = subscriber_config.topic
        binding_key = get_event_binding_key(
            subscriber_config.organization, subscriber_config.service
        )

        create_dead_letter_exchange_and_bind_queue(
            connection=self.connection,
            exchange=exchange,
            queue=queue,
            binding_key=binding_key,
        )
        create_exchange_and_bind_queue(
            connection=self.connection,
            exchange=exchange,
            queue=queue,
            binding_key=binding_key,
            dead_letter=True,
        )

    def unsubscribe_all(self):
        def kill():
            self._channel.stop_consuming()

        if self._is_subscribed:
            self.connection.call_later(0, kill)
            self._thread.join()

    def info(self) -> Dict:
        return {
            "name": self.__class__.__name__,
            "connection.is_open": self.connection.is_open,
        }
