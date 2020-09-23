import threading
import traceback
from time import sleep
from typing import Callable, List

from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from petisco import Event
from petisco.event.shared.domain.event_subscriber import EventSubscriber
from petisco.event.consumer.domain.interface_event_consumer import IEventConsumer
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_exchange_name_formatter import (
    RabbitMqExchangeNameFormatter,
)
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_queue_name_formatter import (
    RabbitMqQueueNameFormatter,
)
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_connector import (
    RabbitMqConnector,
)


class RabbitMqEventConsumer(IEventConsumer):
    def __init__(
        self,
        connector: RabbitMqConnector,
        organization: str,
        service: str,
        max_retries: int,
    ):
        self.connector = connector
        self.exchange_name = f"{organization}.{service}"
        self.max_retries = max_retries
        self._subscribers = []
        self._channels = {}

    def start(self):
        if not self._subscribers:
            raise RuntimeError(
                "RabbitMqEventConsumer: cannot start consuming event without any subscriber defined."
            )
        self._thread = threading.Thread(target=self._start)
        self._thread.start()

    def _start(self):
        self._start_consuming()

    def _start_consuming(self):
        for subscriber in self._subscribers:
            channel_name = self._get_channel_name(subscriber)
            self._channels[channel_name].start_consuming()

    def _get_channel_name(self, subscriber: EventSubscriber):
        queue_name = RabbitMqQueueNameFormatter.format(
            subscriber.event, exchange_name=self.exchange_name
        )
        key_channel = f"{self.exchange_name}.{queue_name}"
        return key_channel

    def consume(self, subscribers: List[EventSubscriber]):
        for subscriber in subscribers:
            queue_name = RabbitMqQueueNameFormatter.format(
                subscriber.event, exchange_name=self.exchange_name
            )

            channel_name = self._get_channel_name(subscriber)
            self._channels[channel_name] = self.connector.get_channel(
                self.exchange_name
            )
            for handler in subscriber.handlers:
                self._channels[channel_name].basic_consume(
                    queue=f"{queue_name}.{handler.__name__}",
                    on_message_callback=self.consumer(handler),
                )

        self._subscribers.extend(subscribers)

    # consumer.consume_dead_letter_from_subscriber(subscriber, dead_letter_consumer)

    def consume_dead_letter(self, subscriber: EventSubscriber, handler: Callable):
        queue_name = RabbitMqQueueNameFormatter.format_dead_letter(
            subscriber.event, exchange_name=self.exchange_name
        )
        for handler_name in subscriber.get_handlers_names():
            channel_name = f"{self.exchange_name}.{queue_name}.{handler_name}"
            self._channels[channel_name] = self.connector.get_channel(
                self.exchange_name
            )
            self._channels[channel_name].basic_consume(
                queue=f"{queue_name}.{handler_name}",
                on_message_callback=self.consumer(handler),
            )

    # self._subscribers.extend(subscribers)

    def consume_queue(self, queue_name: str, handler: Callable):
        channel = self.connector.get_channel(self.exchange_name)

        channel.basic_consume(
            queue=queue_name, on_message_callback=self.consumer(handler)
        )

    def consumer(self, handler: Callable) -> Callable:
        def rabbitmq_consumer(
            ch: BlockingChannel,
            method: Basic.Deliver,
            properties: BasicProperties,
            body: bytes,
        ):
            print(
                "\n#####################################################################################################################"
            )
            print(" [x] Received %r" % (body,))
            print(" [x] Properties %r" % (properties,))
            print(" [x] method %r" % (method,))

            try:
                event = Event.from_json(body)
            except TypeError:
                event = Event.from_deprecated_json(body)
            except:  # noqa E722
                ch.basic_nack(delivery_tag=method.delivery_tag)
                return

            result = handler(event)

            if result is None or result.is_failure:
                if not properties.headers:
                    properties.headers = {
                        "queue": f"{method.routing_key}.{handler.__name__}"
                    }
                self.handle_consumption_error(ch, method, properties, body)
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)

            print(
                "#####################################################################################################################\n"
            )

        return rabbitmq_consumer

    def handle_consumption_error(
        self,
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ):
        if self.has_been_redelivered_too_much(properties):
            self.send_to_dead_letter(ch, method, properties, body)
        else:
            self.send_to_retry(ch, method, properties, body)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def has_been_redelivered_too_much(self, properties: BasicProperties):
        return (
            False
            if not properties.headers or "redelivery_count" not in properties.headers
            else properties.headers.get("redelivery_count") >= self.max_retries
        )

    def _get_routing_key(self, routing_key: str, prefix: str):
        if routing_key.startswith("retry."):
            routing_key = routing_key.replace("retry.", prefix, 1)
        elif routing_key.startswith("dead_letter."):
            routing_key = routing_key.replace("dead_letter.", prefix, 1)
        else:
            routing_key = f"{prefix}{routing_key}"
        return routing_key

    def send_to_retry(
        self,
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ):
        print(" [>] send_to_retry")
        exchange_name = RabbitMqExchangeNameFormatter.retry(self.exchange_name)

        routing_key = method.routing_key
        if properties.headers:
            routing_key = properties.headers.get("queue", routing_key)

        routing_key = self._get_routing_key(routing_key, "retry.")
        self.send_message_to(exchange_name, ch, routing_key, properties, body)

    def send_to_dead_letter(
        self,
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ):
        print(" [>] send_to_dead_letter")
        exchange_name = RabbitMqExchangeNameFormatter.dead_letter(self.exchange_name)
        routing_key = self._get_routing_key(method.routing_key, "dead_letter.")
        self.send_message_to(exchange_name, ch, routing_key, properties, body)

    def send_message_to(
        self,
        exchange_name: str,
        ch: BlockingChannel,
        routing_key: str,
        properties: BasicProperties,
        body: bytes,
    ):
        if properties.headers:
            redelivery_count = properties.headers.get("redelivery_count", 0)
            properties.headers["redelivery_count"] = redelivery_count + 1
        else:
            properties.headers = {"redelivery_count": 1}

        print(f" [>] send: [{exchange_name} |{routing_key}] -> {properties.headers}")
        # ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

        ch.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=body,
            properties=properties,
        )

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

    def _unsubscribe_all(self):
        def _stop_consuming_channels():
            for subscriber in self._subscribers:
                try:
                    channel_name = self._get_channel_name(subscriber)
                    self._channels[channel_name].stop_consuming()
                    self._channels[channel_name].cancel()
                except ValueError:
                    pass

        def _await_for_stop_consuming_channels():
            sleep(2.0)

        self.connector.get_connection(self.exchange_name).call_later(
            0, _stop_consuming_channels
        )
        _await_for_stop_consuming_channels()
