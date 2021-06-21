from examples.rabbitmq.common import ORGANIZATION, SERVICE, UserCreated
from petisco.extra.rabbitmq import RabbitMqConnector, RabbitMqDomainEventBus

connector = RabbitMqConnector()

bus = RabbitMqDomainEventBus(connector, ORGANIZATION, SERVICE)

event = UserCreated.random()

bus.publish(event)
