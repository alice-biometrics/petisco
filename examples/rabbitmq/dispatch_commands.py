from examples.rabbitmq.common import ORGANIZATION, SERVICE, PersistUser
from petisco import Uuid
from petisco.extra.rabbitmq import RabbitMqCommandBus, RabbitMqConnector

connector = RabbitMqConnector()
command_bus = RabbitMqCommandBus(ORGANIZATION, SERVICE, connector)

user_id = Uuid.v4()
command = PersistUser(user_id=user_id)

print("Commands")
print(f"Dispatch {command}")

command_bus.dispatch(command)
