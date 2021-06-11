from examples.rabbitmq.common import ORGANIZATION, SERVICE, subscribers
from petisco.legacy import RabbitMqConnector, RabbitMqEventConfigurer


def configure():
    connector = RabbitMqConnector()

    configurer = RabbitMqEventConfigurer(connector, ORGANIZATION, SERVICE)
    configurer.configure_subscribers(subscribers)


if __name__ == "__main__":
    configure()
