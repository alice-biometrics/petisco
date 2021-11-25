import logging

from examples.rabbitmq.common import MAX_RETRIES, ORGANIZATION, SERVICE, subscribers
from petisco.extra.rabbitmq import RabbitMqConnector, RabbitMqMessageConsumer
from petisco.legacy import LoggingBasedLogger


def get_logger():
    def logging_config():
        logging.getLogger("pika").setLevel(logging.WARNING)

    logger = LoggingBasedLogger("example", config=logging_config)
    return logger


connector = RabbitMqConnector()
consumer = RabbitMqMessageConsumer(
    ORGANIZATION, SERVICE, MAX_RETRIES, connector, logger=get_logger()
)
consumer.add_subscribers(subscribers)

for subscriber in subscribers:
    print(subscriber.__repr__())
print("")

consumer.start()
