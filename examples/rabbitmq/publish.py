from examples.rabbitmq.common import ORGANIZATION, SERVICE, UserCreated
from petisco import RabbitMqConnector
from petisco.event.bus.infrastructure.rabbitmq_event_bus import RabbitMqEventBus

connector = RabbitMqConnector()

bus = RabbitMqEventBus(connector, ORGANIZATION, SERVICE)

event = UserCreated.random()

bus.publish(event)
