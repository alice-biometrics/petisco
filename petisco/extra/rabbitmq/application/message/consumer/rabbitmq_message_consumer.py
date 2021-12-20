import threading
import traceback
from dataclasses import dataclass
from time import sleep
from typing import Callable, List, Optional, Type

from meiga import Failure
from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from petisco.base.domain.message.chaos.message_chaos import MessageChaos
from petisco.base.domain.message.chaos.message_chaos_error import MessageChaosError
from petisco.base.domain.message.chaos.not_implemented_message_chaos import (
    NotImplementedMessageChaos,
)
from petisco.base.domain.message.command import Command
from petisco.base.domain.message.consumer_derived_action import ConsumerDerivedAction
from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.message import Message
from petisco.base.domain.message.message_consumer import MessageConsumer
from petisco.base.domain.message.message_handler_returns_none_error import (
    MessageHandlerReturnsNoneError,
)
from petisco.base.domain.message.message_subscriber import MessageSubscriber
from petisco.extra.rabbitmq.application.message.bus.rabbitmq_command_bus import (
    RabbitMqCommandBus,
)
from petisco.extra.rabbitmq.application.message.bus.rabbitmq_domain_event_bus import (
    RabbitMqDomainEventBus,
)
from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_consumer_connector import (
    RabbitMqConsumerConnector,
)
from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_event_consumer_logger import (
    RabbitMqMessageConsumerLogger,
)
from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_event_consumer_printer import (
    RabbitMqEventConsumerPrinter,
)
from petisco.extra.rabbitmq.application.message.formatter.rabbitmq_message_subscriber_queue_name_formatter import (
    RabbitMqMessageSubscriberQueueNameFormatter,
)
from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector
from petisco.extra.rabbitmq.shared.rabbitmq_exchange_name_formatter import (
    RabbitMqExchangeNameFormatter,
)
from petisco.legacy.logger.interface_logger import ILogger
from petisco.legacy.logger.not_implemented_logger import NotImplementedLogger


@dataclass
class SubscriberItem:
    queue_name: str
    subscriber: MessageSubscriber
    consumer_tag: str
    is_store: bool = False


class RabbitMqMessageConsumer(MessageConsumer):
    def __init__(
        self,
        organization: str,
        service: str,
        max_retries: int,
        connector: RabbitMqConnector = RabbitMqConnector(),
        verbose: bool = False,
        chaos: MessageChaos = NotImplementedMessageChaos(),
        logger: Optional[ILogger] = NotImplementedLogger(),
    ):
        self.connector = connector
        self.organization = organization
        self.service = service
        self.exchange_name = f"{organization}.{service}"
        self.rabbitmq_key = f"consumer-{self.exchange_name}"
        self._fallback_store_exchange_name = f"retry.{organization}.store"
        self.max_retries = max_retries
        self._channel = self.connector.get_channel(self.rabbitmq_key)
        self.printer = RabbitMqEventConsumerPrinter(verbose)
        self.consumer_logger = RabbitMqMessageConsumerLogger(logger)
        self.chaos = chaos
        self.subscribers = {}

    def start(self):
        if not self._channel:
            raise RuntimeError(
                "RabbitMqMessageConsumer: cannot start consuming event without any subscriber defined."
            )
        self._thread = threading.Thread(target=self._start)
        self._thread.start()

    def _start(self):
        self._channel.start_consuming()

    def add_subscribers(self, subscribers: List[Type[MessageSubscriber]]):
        for SubscriberClass in subscribers:

            subscriber: MessageSubscriber = SubscriberClass()

            for subscriber_info in subscriber.get_message_subscribers_info():

                if subscriber_info.message_type == "message":
                    self._add_subscriber_instance_on_queue(
                        queue_name="store", subscriber=subscriber, is_store=True
                    )
                else:
                    queue_name = RabbitMqMessageSubscriberQueueNameFormatter.format(
                        subscriber_info, exchange_name=self.exchange_name
                    )
                    self._add_subscriber_instance_on_queue(
                        queue_name=f"{queue_name}.{subscriber.get_subscriber_name()}",
                        subscriber=subscriber,
                        message_type_expected=subscriber_info.message_type,
                    )

    def add_subscriber_on_dead_letter(self, subscriber: Type[MessageSubscriber]):
        instance_subscriber: MessageSubscriber = subscriber()
        for subscriber_info in instance_subscriber.get_message_subscribers_info():

            queue_name = RabbitMqMessageSubscriberQueueNameFormatter.format_dead_letter(
                subscriber_info, exchange_name=self.exchange_name
            )
            self._add_subscriber_instance_on_queue(
                queue_name=f"{queue_name}.{instance_subscriber.get_subscriber_name()}",
                subscriber=instance_subscriber,
                message_type_expected=subscriber_info.message_type,
            )

    # def add_handler_on_store(self, handler: Callable):
    #     self.add_handler_on_queue("store", handler, is_store=True)

    def _add_subscriber_instance_on_queue(
        self,
        queue_name: str,
        subscriber: MessageSubscriber,
        is_store: bool = False,
        message_type_expected: str = "message",
    ):
        consumer_tag = self._channel.basic_consume(
            queue=queue_name,
            on_message_callback=self.consumer(
                subscriber, is_store, message_type_expected
            ),
        )
        self.subscribers[queue_name] = SubscriberItem(
            queue_name, subscriber, consumer_tag, is_store
        )

    def add_subscriber_on_queue(
        self,
        queue_name: str,
        subscriber: Type[MessageSubscriber],
        is_store: bool = False,
        message_type_expected: str = "message",
    ):
        subscriber: MessageSubscriber = subscriber()
        return self._add_subscriber_instance_on_queue(
            queue_name=queue_name,
            subscriber=subscriber,
            is_store=is_store,
            message_type_expected=message_type_expected,
        )

    def consumer(
        self,
        subscriber: MessageSubscriber,
        is_store: bool = False,
        message_type_expected: str = "message",
    ) -> Callable:
        def rabbitmq_consumer(
            ch: BlockingChannel,
            method: Basic.Deliver,
            properties: BasicProperties,
            body: bytes,
        ):
            self.printer.print_received_message(method, properties, body)

            if self.chaos.nack_simulation(ch, method):
                self.consumer_logger.log_nack_simulation(
                    method, properties, body, subscriber.handle
                )
                return
            else:
                self.consumer_logger.log(
                    method,
                    properties,
                    body,
                    subscriber.handle,
                    log_activity="received_message",
                )

            try:
                if message_type_expected == "domain_event":
                    message = DomainEvent.from_json(body)
                elif message_type_expected == "command":
                    message = Command.from_json(body)
                else:
                    message = Message.from_json(body)
            except Exception as e:
                self.consumer_logger.log_parser_error(
                    method, properties, body, subscriber.handle, e
                )
                ch.basic_nack(delivery_tag=method.delivery_tag)
                return

            self.chaos.delay()

            if self.chaos.failure_simulation(method):
                self.consumer_logger.log_failure_simulation(
                    method, properties, body, subscriber.handle
                )
                result = Failure(MessageChaosError())
            else:
                connector = RabbitMqConsumerConnector(ch)
                domain_event_bus = RabbitMqDomainEventBus(
                    self.organization, self.service, connector
                )
                command_bus = RabbitMqCommandBus(
                    self.organization, self.service, connector
                )
                subscriber.set_domain_event_bus(domain_event_bus)
                subscriber.set_command_bus(command_bus)

                result = subscriber.handle(message)

            self.printer.print_context(subscriber.handle, result)

            if result is None:
                raise MessageHandlerReturnsNoneError(subscriber.handle)

            derived_action = ConsumerDerivedAction()
            if result.is_failure:
                if not properties.headers:
                    properties.headers = {
                        "queue": f"{method.routing_key}.{subscriber.get_subscriber_name()}"
                    }
                derived_action = self.handle_consumption_error(
                    ch, method, properties, body, is_store
                )
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)

            self.consumer_logger.log(
                method,
                properties,
                body,
                subscriber.handle,
                "computed_message",
                result,
                derived_action,
            )
            self.printer.print_separator()

        return rabbitmq_consumer

    def handle_consumption_error(
        self,
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
        is_store: bool,
    ):

        if self.has_been_redelivered_too_much(properties):
            derived_action = self.send_to_dead_letter(ch, method, properties, body)
        else:
            derived_action = self.send_to_retry(ch, method, properties, body, is_store)

        ch.basic_ack(delivery_tag=method.delivery_tag)

        return derived_action

    def has_been_redelivered_too_much(self, properties: BasicProperties):
        if not properties.headers or "redelivery_count" not in properties.headers:
            if self.max_retries < 1:
                return True
            return False
        else:
            return properties.headers.get("redelivery_count") >= self.max_retries

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
        is_store: bool = False,
    ):
        self.printer.print_action("send_to_retry")
        exchange_name = RabbitMqExchangeNameFormatter.retry(self.exchange_name)

        routing_key = method.routing_key
        if properties.headers:
            routing_key = properties.headers.get("queue", routing_key)

        if is_store:
            routing_key = "store"
            exchange_name = self._fallback_store_exchange_name

        routing_key = self._get_routing_key(routing_key, "retry.")

        updated_headers = self.send_message_to(
            exchange_name, ch, routing_key, properties, body
        )
        return ConsumerDerivedAction(
            action="send_to_retry",
            exchange_name=exchange_name,
            routing_key=routing_key,
            headers=updated_headers,
        )

    def send_to_dead_letter(
        self,
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ):
        self.printer.print_action("send_to_dead_letter")
        exchange_name = RabbitMqExchangeNameFormatter.dead_letter(self.exchange_name)
        routing_key = self._get_routing_key(method.routing_key, "dead_letter.")
        updated_headers = self.send_message_to(
            exchange_name, ch, routing_key, properties, body
        )
        return ConsumerDerivedAction(
            action="send_to_dead_letter",
            exchange_name=exchange_name,
            routing_key=routing_key,
            headers=updated_headers,
        )

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

        self.printer.print_send_message_to(
            exchange_name, routing_key, properties.headers
        )

        ch.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=body,
            properties=properties,
        )

        return properties.headers

    def stop(self):
        def _log_stop_exception(e: Exception):
            from petisco.legacy import ERROR, LogMessage, Petisco

            logger = Petisco.get_logger()
            log_message = LogMessage(
                layer="petisco", operation="RabbitMQEventSubscriber"
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
        def _stop_consuming_consumer_channel():
            try:
                self._channel.stop_consuming()
                self._channel.cancel()
            except ValueError:
                pass

        def _await_for_stop_consuming_consumer_channel():
            sleep(2.0)

        self.connector.get_connection(self.rabbitmq_key).call_later(
            0, _stop_consuming_consumer_channel
        )

        _await_for_stop_consuming_consumer_channel()

    def unsubscribe_subscriber_on_queue(self, queue_name: str):
        subscriber_item: SubscriberItem = self.subscribers.get(queue_name)
        if subscriber_item is None:
            raise IndexError(
                f"Cannot unsubscribe an nonexistent queue ({queue_name}). Please, check configured consumers ({list(self.subscribers.keys())})"
            )

        def _unsubscribe_handler_on_queue():
            self._channel.basic_cancel(consumer_tag=subscriber_item.consumer_tag)

        self._do_it_in_consumer_thread(_unsubscribe_handler_on_queue)

    def resume_subscriber_on_queue(self, queue_name: str):
        subscriber_item: SubscriberItem = self.subscribers.get(queue_name)
        if subscriber_item is None:
            raise IndexError(
                f"Cannot resume an nonexistent queue ({queue_name}). Please, check configured consumers ({list(self.subscribers.keys())})"
            )

        def _resume_handler_on_queue():
            subscriber_item.consumer_tag = self._channel.basic_consume(
                queue=subscriber_item.queue_name,
                on_message_callback=self.consumer(
                    subscriber_item.subscriber, subscriber_item.is_store
                ),
            )

        self._do_it_in_consumer_thread(_resume_handler_on_queue)

    def _do_it_in_consumer_thread(self, action: Callable):
        def _execute_action():
            try:
                action()
            except ValueError:
                pass

        def _await_for_thread():
            sleep(2.0)

        self.connector.get_connection(self.rabbitmq_key).call_later(0, _execute_action)

        _await_for_thread()
