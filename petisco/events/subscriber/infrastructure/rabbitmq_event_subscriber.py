import threading
import traceback
from time import sleep
from typing import Dict

from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import StreamLostError

from petisco.events.rabbitmq.create_exchange_and_bind_queue import (
    create_exchange_and_bind_queue,
    create_dead_letter_exchange_and_bind_queue,
)
from petisco.events.rabbitmq.get_event_binding_key import get_event_binding_key
from petisco.events.rabbitmq.rabbitmq_connector import RabbitMQConnector
from petisco.events.subscriber.domain.config_event_subscriber import (
    ConfigEventSubscriber,
)
from petisco.events.subscriber.domain.interface_event_subscriber import IEventSubscriber


class RabbitMQEventSubscriber(IEventSubscriber):
    def __init__(
        self,
        connector: RabbitMQConnector,
        subscribers: Dict[str, ConfigEventSubscriber] = None,
        connection_name: str = "subscriber",
    ):
        if not connector:
            raise TypeError("RabbitMQEventSubscriber: Invalid Given RabbitMQConnector")

        self._connector = connector
        self._connection = None
        self._connection_name = connection_name
        self._channels = {}
        self._thread = None
        super().__init__(subscribers)

    def start(self):
        if not self.subscribers:
            raise RuntimeError(
                "RabbitMQEventSubscriber: cannot start consuming events without any subscriber defined"
            )
        self._thread = threading.Thread(target=self._start)
        self._thread.start()

    def _start(self):
        self._connect()
        self._create_channels()
        self._bind_queue_and_subscribers()
        self._start_consuming()

    def _connect(self):
        self._connection = self._connector.get_connection(self._connection_name)

    def _check_connection(self):
        if not self._connection.is_open:
            self._connect()

    def _get_channel(self) -> BlockingChannel:
        self._check_connection()
        try:
            channel = self._connection.channel()
        except StreamLostError:
            self._check_connection()
            channel = self._connection.channel()
        return channel

    def _create_channels(self):
        # This uses the basic.qos protocol method to tell RabbitMQ not to give more than one message to a worker at a
        # time. Or, in other words, don't dispatch a new message to a worker until it has processed and acknowledged
        # the previous one. Instead, it will dispatch it to the next worker that is not still busy.
        for name in self.subscribers.keys():
            self._channels[name] = self._get_channel()
            self._channels[name].basic_qos(prefetch_count=1)

    def _bind_queue_and_subscribers(self):
        for name, subscriber_config in self.subscribers.items():
            self._setup_exchanges_and_queues(subscriber_config, self._channels[name])
            queue = (
                subscriber_config.topic
                if not subscriber_config.dead_letter
                else f"dl-{subscriber_config.topic}"
            )
            self._channels[name].basic_consume(
                queue=queue, on_message_callback=subscriber_config.get_handler()
            )

    def _setup_exchanges_and_queues(
        self, subscriber_config: ConfigEventSubscriber, channel: BlockingChannel
    ):
        exchange = subscriber_config.service
        queue = subscriber_config.topic
        binding_key = get_event_binding_key(
            subscriber_config.organization, subscriber_config.service
        )

        create_dead_letter_exchange_and_bind_queue(
            channel=channel, exchange=exchange, queue=queue, binding_key=binding_key
        )
        create_exchange_and_bind_queue(
            channel=channel,
            exchange=exchange,
            queue=queue,
            binding_key=binding_key,
            dead_letter=True,
        )

    def _start_consuming(self):
        for name in self.subscribers.keys():
            self._channels[name].start_consuming()

    def get_subscribers_status(self) -> Dict[str, str]:
        subscribers_status = {}
        for name, channel in self._channels.items():
            subscribers_status[name] = (
                "subscribed" if len(channel.consumer_tags) > 0 else "unsubscribed"
            )
        return subscribers_status

    def _unsubscribe_all(self):
        def _stop_consuming_channels():
            for name in self.subscribers.keys():
                if name in self._channels:
                    self._channels[name].stop_consuming()
                    self._channels[name].cancel()

        def _await_for_stop_consuming_channels():
            sleep(2.0)

        self._connection.call_later(0, _stop_consuming_channels)
        _await_for_stop_consuming_channels()

    def stop(self):
        def _log_stop_exception(e: Exception):
            from petisco import LogMessage, ERROR, Petisco

            logger = Petisco.get_logger()
            log_message = LogMessage(
                layer="petisco", operation=f"RabbitMQEventSubscriber"
            )
            message = f"Error stopping RabbitMQEventSubscriber: {repr(e.__class__)} {e} | {traceback.format_exc()}"
            logger.log(ERROR, log_message.set_message(message))

        if self._thread and self._thread.is_alive():
            self._unsubscribe_all()
            try:
                self._thread.join()
                self._thread = None
            except Exception as e:
                _log_stop_exception(e)

    def info(self) -> Dict:
        is_open = False
        if self._connection:
            is_open = self._connection.is_open
        return {
            "name": self.__class__.__name__,
            "connection.is_open": is_open,
            "subscribers_status": self.get_subscribers_status(),
        }
