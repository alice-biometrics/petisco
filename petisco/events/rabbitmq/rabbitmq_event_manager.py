import threading
from typing import Dict, Callable

from pika import BlockingConnection, ConnectionParameters, BasicProperties

from petisco.events.event import Event
from petisco.events.interface_event_manager import IEventManager


class RabbitMQEventManager(IEventManager):
    def __init__(
        self,
        connection_parameters: ConnectionParameters,
        subscribers: Dict[str, Callable] = None,
    ):
        super().__init__(subscribers)
        self.connection_parameters = connection_parameters

        if self.subscribers:
            # Run the worker into a thread
            self._thread = threading.Thread(target=self._subscribe)
            self._thread.start()

    def info(self) -> Dict:
        return {
            "name": self.__class__.__name__,
            "host": self.connection_parameters._host,
            "port": self.connection_parameters._port,
        }

    def _subscribe(self):
        self._connection_subscriber = BlockingConnection(self.connection_parameters)
        self._channel_subscriber = self._connection_subscriber.channel()
        self._channel_subscriber.basic_qos(prefetch_count=1)

        for topic, callback in self.subscribers.items():
            self._channel_subscriber.queue_declare(queue=topic, durable=True)
            self._channel_subscriber.basic_consume(
                queue=topic, on_message_callback=callback
            )

        self._channel_subscriber.start_consuming()

    def unsubscribe_all(self):
        def kill():
            self._channel_subscriber.stop_consuming()

        if self.subscribers:
            self._connection_subscriber.call_later(0, kill)
            self._thread.join()

    def send(self, topic: str, event: Event):
        connection_publisher = BlockingConnection(self.connection_parameters)
        channel = connection_publisher.channel()
        channel.queue_declare(queue=topic, durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=topic,
            body=event.to_json(),
            properties=BasicProperties(delivery_mode=2),  # make message persistent
        )
        connection_publisher.close()
