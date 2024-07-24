from argparse import ArgumentParser

from common import ORGANIZATION, SERVICE, UserCreated

from petisco import Uuid
from petisco.extra.rabbitmq import RabbitMqConnector, RabbitMqDomainEventBus

connector = RabbitMqConnector()
domain_event_bus = RabbitMqDomainEventBus(ORGANIZATION, SERVICE, connector)


def main(number_events: int) -> None:
    print(f"Domain Events [{number_events}]")
    for _ in range(number_events):
        user_id = Uuid.v4()
        user_created = UserCreated(user_id=user_id)
        print(f"Publish {user_created}")
        domain_event_bus.publish(user_created)


if __name__ == "__main__":
    parser = ArgumentParser(description="Publish a specified number of domain events.")
    parser.add_argument("-n", "--number", type=int, default=1, help="Number of times to perform the action")

    args = parser.parse_args()
    main(args.number)
