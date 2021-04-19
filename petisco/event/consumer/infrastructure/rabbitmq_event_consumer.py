import inspect
import threading
import traceback
from time import sleep
from typing import Callable, List, Optional

from dataclasses import dataclass
from meiga import Failure
from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from petisco.event.bus.infrastructure.rabbitmq_consumer_event_bus import (
    RabbitMqConsumerEventBus,
)
from petisco.event.chaos.domain.event_chaos_error import EventChaosError
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_consumer_connector import (
    RabbitMqConsumerConnector,
)
from petisco.logger.interface_logger import ILogger
from petisco.logger.not_implemented_logger import NotImplementedLogger

from petisco.event.chaos.domain.interface_event_chaos import IEventChaos
from petisco.event.chaos.infrastructure.not_implemented_event_chaos import (
    NotImplementedEventChaos,
)

from petisco.event.consumer.domain.consumer_derived_action import ConsumerDerivedAction
from petisco.event.consumer.infrastructure.rabbitmq_event_consumer_logger import (
    RabbitMqEventConsumerLogger,
)
from petisco.event.consumer.infrastructure.rabbitmq_event_consumer_printer import (
    RabbitMqEventConsumerPrinter,
)
from petisco.event.consumer.infrastructure.rabbitmq_event_consumer_return_error import (
    RabbitMqEventConsumerReturnError,
)
from petisco.event.shared.domain.event import Event
from petisco.event.shared.domain.event_subscriber import EventSubscriber
from petisco.event.consumer.domain.interface_event_consumer import IEventConsumer
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_exchange_name_formatter import (
    RabbitMqExchangeNameFormatter,
)
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_event_subscriber_queue_name_formatter import (
    RabbitMqEventSubscriberQueueNameFormatter,
)
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_connector import (
    RabbitMqConnector,
)


@dataclass
class HandlerItem:
    queue_name: str
    handler: Callable
    consumer_tag: str
    is_store: bool = False


class RabbitMqEventConsumer(IEventConsumer):
    def __init__(
        self,
        connector: RabbitMqConnector,
        organization: str,
        service: str,
        max_retries: int,
        verbose: bool = False,
        chaos: IEventChaos = NotImplementedEventChaos(),
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
        self.consumer_logger = RabbitMqEventConsumerLogger(logger)
        self.chaos = chaos
        self.handlers = {}

    def start(self):
        if not self._channel:
            raise RuntimeError(
                "RabbitMqEventConsumer: cannot start consuming event without any subscriber defined."
            )

        self._thread = threading.Thread(target=self._start)
        self._thread.start()

    def _start(self):
        self._channel.start_consuming()

    def add_subscribers(self, subscribers: List[EventSubscriber]):
        for subscriber in subscribers:
            queue_name = RabbitMqEventSubscriberQueueNameFormatter.format(
                subscriber, exchange_name=self.exchange_name
            )
            for handler in subscriber.handlers:
                self.add_handler_on_queue(
                    queue_name=f"{queue_name}.{handler.__name__}", handler=handler
                )

    def add_subscriber_on_dead_letter(
        self, subscriber: EventSubscriber, handler: Callable
    ):
        queue_name = RabbitMqEventSubscriberQueueNameFormatter.format_dead_letter(
            subscriber, exchange_name=self.exchange_name
        )
        for handler_name in subscriber.get_handlers_names():
            self.add_handler_on_queue(
                queue_name=f"{queue_name}.{handler_name}", handler=handler
            )

    def add_handler_on_store(self, handler: Callable):
        self.add_handler_on_queue("store", handler, is_store=True)

    def add_handler_on_queue(
        self, queue_name: str, handler: Callable, is_store: bool = False
    ):
        consumer_tag = self._channel.basic_consume(
            queue=queue_name, on_message_callback=self.consumer(handler, is_store)
        )
        self.handlers[queue_name] = HandlerItem(
            queue_name, handler, consumer_tag, is_store
        )

    def consumer(self, handler: Callable, is_store: bool = False) -> Callable:
        def rabbitmq_consumer(
            ch: BlockingChannel,
            method: Basic.Deliver,
            properties: BasicProperties,
            body: bytes,
        ):
            self.printer.print_received_message(method, properties, body)

            if self.chaos.nack_simulation(ch, method):
                self.consumer_logger.log_nack_simulation(
                    method, properties, body, handler
                )
                return
            else:
                self.consumer_logger.log(
                    method, properties, body, handler, log_activity="received_message"
                )

            try:
                event = Event.from_json(body)
            except TypeError:
                event = Event.from_deprecated_json(body)
            except Exception as e:
                self.consumer_logger.log_parser_error(
                    method, properties, body, handler, e
                )
                ch.basic_nack(delivery_tag=method.delivery_tag)
                return

            self.chaos.delay()

            if self.chaos.failure_simulation(method):
                self.consumer_logger.log_failure_simulation(
                    method, properties, body, handler
                )
                result = Failure(EventChaosError())
            else:
                params = inspect.getfullargspec(handler).args
                if "event_bus" in params:
                    connector = RabbitMqConsumerConnector(ch)
                    event_bus = RabbitMqConsumerEventBus(
                        connector, self.organization, self.service
                    )
                    result = handler(event, event_bus)
                else:
                    result = handler(event)

            self.printer.print_context(handler, result)

            if result is None:
                raise RabbitMqEventConsumerReturnError(handler)

            derived_action = ConsumerDerivedAction()
            if result.is_failure:
                if not properties.headers:
                    properties.headers = {
                        "queue": f"{method.routing_key}.{handler.__name__}"
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
                handler,
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
            from petisco import LogMessage, ERROR, Petisco

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

    def unsubscribe_handler_on_queue(self, queue_name: str):
        handler_item: HandlerItem = self.handlers.get(queue_name)
        if handler_item is None:
            raise IndexError(
                f"Cannot unsubscribe an nonexistent queue ({queue_name}). Please, check configured consumers ({list(self.handlers.keys())})"
            )

        def _unsubscribe_handler_on_queue():
            self._channel.basic_cancel(consumer_tag=handler_item.consumer_tag)

        self._do_it_in_consumer_thread(_unsubscribe_handler_on_queue)

    def resume_handler_on_queue(self, queue_name: str):
        handler_item: HandlerItem = self.handlers.get(queue_name)
        if handler_item is None:
            raise IndexError(
                f"Cannot resume an nonexistent queue ({queue_name}). Please, check configured consumers ({list(self.handlers.keys())})"
            )

        def _resume_handler_on_queue():
            handler_item.consumer_tag = self._channel.basic_consume(
                queue=handler_item.queue_name,
                on_message_callback=self.consumer(
                    handler_item.handler, handler_item.is_store
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
