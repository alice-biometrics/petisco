from examples.rabbitmq.common import ORGANIZATION, SERVICE, UserCreated
from petisco.legacy import RabbitMqConnector
from petisco.legacy.event.bus.infrastructure.rabbitmq_event_bus import RabbitMqEventBus

connector = RabbitMqConnector()

bus = RabbitMqEventBus(connector, ORGANIZATION, SERVICE)

event = UserCreated.random()

bus.publish(event)
