import argparse
import logging
from time import sleep
from typing import Any, List, Type, cast

from meiga import BoolResult, isFailure, isSuccess

from petisco import (
    AllMessageSubscriber,
    DomainEvent,
    Message,
    MessageSubscriber,
    __version__,
)
from petisco.extra.logger import Logger, LoggingBasedLogger
from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_message_consumer import (
    RabbitMqMessageConsumer,
)
from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector

ORGANIZATION = "alice"
RETRY_TTL = 5000  # default
MAX_RETRIES = 5  # default


def has_args(args: Any) -> bool:
    is_active = False
    for arg in vars(args):
        is_active = is_active or getattr(args, arg)
    return is_active


def get_logger() -> Logger:
    def logging_config() -> None:
        logging.getLogger("pika").setLevel(logging.WARNING)

    logger = LoggingBasedLogger("example", config=logging_config)
    return logger


class MyDomainEvent(DomainEvent): ...


class UnackMessage(MessageSubscriber):
    def subscribed_to(self) -> List[Type[Message]]:
        return [MyDomainEvent]

    def handle(self, message: Message) -> BoolResult:
        print(f"> It will unack the message: {message.format()}\n")
        return isFailure


def get_args() -> Any:
    parser = argparse.ArgumentParser(
        prog="petisco-rabbitmq 🍪",
        description="petisco-rabbitmq helps us on rabbitmq iteration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-rq", "--requeue", action="store_true", help="requeue")
    parser.add_argument(
        "-o",
        "--organization",
        action="store",
        dest="organization",
        default=ORGANIZATION,
        help="Name of the organization",
    )
    parser.add_argument(
        "-s",
        "--service",
        action="store",
        dest="service",
        default=None,
        help="Name of the service",
    )
    parser.add_argument(
        "-cq",
        "--consuming-queue",
        action="store",
        dest="consuming_queue",
        default=None,
        help="Queue to consume",
    )
    parser.add_argument(
        "-rrk",
        "--retry-routing-key",
        action="store",
        dest="retry_routing_key",
        default=None,
        help="Routing key to republish the message to specific retry queue",
    )
    parser.add_argument(
        "-ren",
        "--retry-exchange-name",
        action="store",
        dest="retry_exchange_name",
        default=None,
        help="Exchange name to republish the message to specific exchange",
    )
    parser.add_argument(
        "-mr",
        "--max-retries",
        action="store",
        dest="max_retries",
        default=MAX_RETRIES,
        help="Max Retries",
    )
    parser.add_argument(
        "-rttl",
        "--retry-ttl",
        action="store",
        dest="retry_ttl",
        default=RETRY_TTL,
        help="Retry TTL",
    )
    parser.add_argument(
        "-wtr",
        "--wait-to-requeue",
        action="store",
        dest="wait_to_requeue",
        default=None,
        help="Wait to Requeue (seconds)",
    )

    args = parser.parse_args()

    if not has_args(args):
        parser.print_help()
        return None

    return args


def main() -> None:
    args = get_args()

    if not args:
        return

    if args.requeue:
        if not args.consuming_queue:
            print(" ➜ Not consuming queue given")
            return

        if not args.retry_routing_key:
            print(" ➜ Not retry routing_key given")
            return

        if not args.service:
            print(" ➜  Not service provided")
            return

        print(f"petisco-rabbitmq ({__version__}) 🍪 ")
        print(f"🍪 Requeuing events from: {args.consuming_queue}")
        print(f"🍪 With the following routing_key: {args.retry_routing_key}")
        if args.retry_exchange_name:
            print(f"🍪 With retry exchange name: {args.retry_exchange_name}")
        print(f"🍪 ORGANIZATION {args.organization}")
        print(f"🍪 SERVICE {args.service}")
        print(f"🍪 MAX_RETRIES {args.max_retries}")
        print(f"🍪 WAIT_TO_REQUEUE {args.wait_to_requeue} seconds")

        connector = RabbitMqConnector()
        consumer = RabbitMqMessageConsumer(
            args.organization,
            args.service,
            args.max_retries,
            connector,
            logger=get_logger(),
        )

        class RequeueOnMessage(AllMessageSubscriber):
            def handle(self, message: Message) -> BoolResult:
                if args.wait_to_requeue:
                    sleep(args.wait_sec)

                message = cast(DomainEvent, message)

                self.domain_event_bus.retry_publish(message, args.retry_routing_key, args.retry_exchange_name)

                return isSuccess

        consumer.add_subscriber_on_queue(
            queue_name=args.consuming_queue,
            subscriber=RequeueOnMessage,
            message_type_expected="domain_event",
        )

        consumer.start()
