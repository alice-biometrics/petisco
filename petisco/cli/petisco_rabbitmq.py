import argparse
import logging
from time import sleep
from typing import List, Type

from meiga import BoolResult, isFailure, isSuccess

from petisco import (
    AllMessageSubscriber,
    DomainEvent,
    Message,
    MessageSubscriber,
    __version__,
)
from petisco.extra.rabbitmq import RabbitMqConnector, RabbitMqMessageConsumer
from petisco.legacy import LoggingBasedLogger

ORGANIZATION = "alice"
RETRY_TTL = 5000  # default
MAX_RETRIES = 5  # default


def has_args(args):
    is_active = False
    for arg in vars(args):
        is_active = is_active or getattr(args, arg)
    return is_active


def get_logger():
    def logging_config():
        logging.getLogger("pika").setLevel(logging.WARNING)

    logger = LoggingBasedLogger("example", config=logging_config)
    return logger


class MyDomainEvent(DomainEvent):
    ...


class UnackMessage(MessageSubscriber):
    def subscribed_to(self) -> List[Type[Message]]:
        return [MyDomainEvent]

    def handle(self, message: Message) -> BoolResult:
        print(f"> It will unack the message: {message.dict()}\n")
        return isFailure


def get_args():
    parser = argparse.ArgumentParser(
        prog="petisco-rabbitmq 🍪",
        description="petisco-rabbitmq helps us on rabbitmq iteration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-rq", "--requeue", action="store_true", help="requeue")
    parser.add_argument(
        "-cq",
        "--consuming-queues",
        action="store",
        dest="consuming_queues",
        default=None,
        help="List of queues to consume split by commas (my-queue-1,my-queue-2)",
    )
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


def main():
    args = get_args()

    if not args:
        return

    if args.requeue:

        if not args.consuming_queues:
            print(" ➜ Not consuming queues given")
            return

        consuming_queues = args.consuming_queues.split(",")

        if not args.service:
            print(" ➜  Not service provided")
            return

        print(f"petisco-rabbitmq ({__version__}) 🍪 ")
        print(f"🍪 Requeuing events from {consuming_queues}")
        print(f"🍪 ORGANIZATION {args.organization}")
        print(f"🍪 SERVICE {args.service}")
        print(f"🍪 MAX_RETRIES {args.max_retries}")
        print(f"🍪 WAIT_TO_REQUEUE {args.wait_to_requeue} seconds")

        class RequeueOnMessage(AllMessageSubscriber):
            def handle(self, message: Message) -> BoolResult:
                if args.wait_to_requeue:
                    sleep(args.wait_sec)
                self.domain_event_bus.publish(message)
                return isSuccess

        connector = RabbitMqConnector()
        consumer = RabbitMqMessageConsumer(
            args.organization,
            args.service,
            args.max_retries,
            connector,
            logger=get_logger(),
        )
        for queue_name in consuming_queues:
            consumer.add_subscriber_on_queue(
                queue_name=queue_name,
                subscriber=RequeueOnMessage,
                message_type_expected="domain_event",
            )

        consumer.start()
