from time import sleep

from examples.rabbitmq.common import ORGANIZATION, SERVICE, UserCreated, UserConfirmed
from petisco import Uuid
from petisco.extra.rabbitmq import RabbitMqConnector, RabbitMqDomainEventBus

connector = RabbitMqConnector()
domain_event_bus = RabbitMqDomainEventBus(connector, ORGANIZATION, SERVICE)

user_id = Uuid.v4()
user_created = UserCreated(user_id=user_id)
user_confirmed = UserConfirmed(user_id=user_id)

print("Domain Events")
print(f"Publish {user_created}")
domain_event_bus.publish(user_created)
print("waiting...")
sleep(3)
print(f"Publish {user_confirmed}\n")
domain_event_bus.publish(user_confirmed)
