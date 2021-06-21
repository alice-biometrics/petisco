import logging

from examples.rabbitmq.common import (
    ORGANIZATION,
    SERVICE,
    MAX_RETRIES,
    subscribers,
    message_store,
)
from petisco.extra.rabbitmq import RabbitMqConnector, RabbitMqMessageConsumer
from petisco.legacy import LoggingBasedLogger


def get_logger():
    def logging_config():
        logging.getLogger("pika").setLevel(logging.WARNING)

    logger = LoggingBasedLogger("example", config=logging_config)
    return logger


connector = RabbitMqConnector()
consumer = RabbitMqMessageConsumer(
    connector, ORGANIZATION, SERVICE, MAX_RETRIES, logger=get_logger()
)
consumer.add_subscribers(subscribers)
consumer.add_handler_on_store(message_store)

for subscriber in subscribers:
    print(subscriber)

consumer.start()
