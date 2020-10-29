from typing import Callable, Optional

from meiga import Result
from pika import BasicProperties
from pika.spec import Basic

from petisco.logger.interface_logger import ILogger, DEBUG
from petisco.logger.log_message import LogMessage
from petisco.logger.not_implemented_logger import NotImplementedLogger

from petisco.event.consumer.domain.consumer_derived_action import ConsumerDerivedAction


class RabbitMqEventConsumerLogger:
    def __init__(self, logger: Optional[ILogger] = NotImplementedLogger()):
        self.logger = logger

    def _get_base_message(self, handler: Callable):
        return LogMessage(
            layer="rabbitmq_event_consumer", operation=f"{handler.__name__}"
        )

    def _get_event_handler_name(self, handler: Callable):
        handler_name = getattr(handler, "__name__", repr(handler))
        handler_module = getattr(handler, "__module__") + "."
        return f"{handler_module}{handler_name}"

    def log_nack_simulation(
        self,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
        handler: Callable,
    ):
        log_message = self._get_base_message(handler)
        event_handler_name = self._get_event_handler_name(handler)
        message = {
            "body": body,
            "properties": properties,
            "method": method,
            "event_handler": event_handler_name,
            "chaos_action": f"nck simulated",
        }
        self.logger.log(DEBUG, log_message.set_message(message))

    def log(
        self,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
        handler: Callable,
        result: Result,
        derived_action: ConsumerDerivedAction(),
    ):
        log_message = self._get_base_message(handler)
        event_handler_name = self._get_event_handler_name(handler)

        message = {
            "body": body,
            "properties": properties,
            "method": method,
            "event_handler": event_handler_name,
            "result": result,
            "derived_action": derived_action.to_dict(),
        }
        self.logger.log(DEBUG, log_message.set_message(message))
