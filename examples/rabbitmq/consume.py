from examples.rabbitmq.common import MAX_RETRIES, ORGANIZATION, SERVICE, subscribers
from petisco.extra.logger import LoguruLogger
from petisco.extra.rabbitmq import RabbitMqConnector, RabbitMqMessageConsumer

connector = RabbitMqConnector()
consumer = RabbitMqMessageConsumer(
    ORGANIZATION, SERVICE, MAX_RETRIES, connector, logger=LoguruLogger()
)
consumer.add_subscribers(subscribers)

for subscriber in subscribers:
    print(subscriber.__repr__())
print("")

consumer.start()
