from examples.rabbitmq.common import ORGANIZATION, SERVICE, MAX_RETRIES, subscribers
from petisco import RabbitMqConnector, RabbitMqEventConsumer

connector = RabbitMqConnector()
consumer = RabbitMqEventConsumer(connector, ORGANIZATION, SERVICE, MAX_RETRIES)
consumer.add_subscribers(subscribers)

consumer.start()
