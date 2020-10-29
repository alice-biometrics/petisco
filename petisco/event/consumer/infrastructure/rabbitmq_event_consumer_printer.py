from typing import Callable, Dict

from meiga import Result
from pika import BasicProperties
from pika.spec import Basic


class RabbitMqEventConsumerPrinter:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def print_received_message(
        self, method: Basic.Deliver, properties: BasicProperties, body: bytes
    ):
        if self.verbose:
            print(
                "\n#####################################################################################################################"
            )
            print(" [x] Received %r" % (body,))
            print(" [x] Properties %r" % (properties,))
            print(" [x] method %r" % (method,))

    def print_separator(self):
        if self.verbose:
            print(
                "#####################################################################################################################\n"
            )

    def print_context(self, handler: Callable, result: Result):
        if self.verbose:
            handler_name = getattr(handler, "__name__", repr(handler))
            handler_module = getattr(handler, "__module__") + "."

            print(f" [x] event_handler: {handler_module}{handler_name}")
            print(f" [x] result from event_handler: {result}")

    def print_action(self, action_name: str):
        if self.verbose:
            print(f" [>] {action_name}")

    def print_send_message_to(
        self, exchange_name: str, routing_key: str, headers: Dict
    ):
        if self.verbose:
            print(f" [>] send: [{exchange_name} |{routing_key}] -> {headers}")
