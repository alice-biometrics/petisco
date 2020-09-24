from examples.rabbitmq.common import ORGANIZATION, SERVICE, subscribers, RETRY_TTL
from petisco import RabbitMqConnector, RabbitMqEventConfigurer


def configure():
    connector = RabbitMqConnector()

    configurer = RabbitMqEventConfigurer(
        connector, ORGANIZATION, SERVICE, retry_ttl=RETRY_TTL
    )
    configurer.configure_subscribers(subscribers)


if __name__ == "__main__":
    configure()
