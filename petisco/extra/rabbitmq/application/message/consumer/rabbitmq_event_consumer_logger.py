from typing import Any, Callable, Optional

from meiga import AnyResult
from pika import BasicProperties
from pika.spec import Basic

from petisco.base.domain.message.consumer_derived_action import ConsumerDerivedAction
from petisco.extra.logger.log_message import LogMessage
from petisco.extra.logger.logger import DEBUG, Logger
from petisco.extra.logger.not_implemented_logger import NotImplementedLogger


class RabbitMqMessageConsumerLogger:
    def __init__(self, logger: Optional[Logger] = NotImplementedLogger()) -> None:
        self.logger = logger

    def _get_base_message(self, handler: Callable[..., Any]) -> LogMessage:
        return LogMessage(layer="rabbitmq_message_consumer", operation=f"{handler.__name__}")

    def _get_event_handler_name(self, handler: Callable[..., Any]) -> str:
        handler_name = getattr(handler, "__name__", repr(handler))
        handler_module = handler.__module__ + "."
        return f"{handler_module}{handler_name}"

    def log_nack_simulation(
        self,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
        handler: Callable[..., Any],
    ) -> None:
        self._log_simulation(method, properties, body, handler, "nack simulated")

    def log_failure_simulation(
        self,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
        handler: Callable[..., Any],
    ) -> None:
        self._log_simulation(method, properties, body, handler, "failure simulated")

    def _log_simulation(
        self,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
        handler: Callable[..., Any],
        chaos_action: str,
    ) -> None:
        log_message = self._get_base_message(handler)
        event_handler_name = self._get_event_handler_name(handler)
        message = {
            "body": body,
            "properties": properties,
            "method": method,
            "event_handler": event_handler_name,
            "chaos_action": chaos_action,
        }
        self.logger.log(DEBUG, log_message.set_message(message))

    def log_parser_error(
        self,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
        handler: Callable[..., Any],
        exception: Exception,
    ) -> None:
        log_message = self._get_base_message(handler)
        event_handler_name = self._get_event_handler_name(handler)
        message = {
            "body": body,
            "properties": properties,
            "method": method,
            "event_handler": event_handler_name,
            "exception": str(exception),
        }
        self.logger.log(DEBUG, log_message.set_message(message))

    def log(
        self,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
        handler: Callable[..., Any],
        log_activity: str = None,
        result: AnyResult = None,
        derived_action: ConsumerDerivedAction() = None,
    ) -> None:
        log_message = self._get_base_message(handler)
        event_handler_name = self._get_event_handler_name(handler)

        message = {
            "body": body,
            "properties": properties,
            "method": method,
            "event_handler": event_handler_name,
        }
        if log_activity:
            message["log_activity"] = log_activity
        if result:
            message["result"] = result
        if derived_action:
            message["derived_action"] = derived_action.dict()

        self.logger.log(DEBUG, log_message.set_message(message))
