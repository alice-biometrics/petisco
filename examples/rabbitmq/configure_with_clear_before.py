from examples.rabbitmq.common import ORGANIZATION, SERVICE, subscribers
from petisco import RabbitMqConnector, RabbitMqEventConfigurer


def configure():
    connector = RabbitMqConnector()

    configurer = RabbitMqEventConfigurer(connector, ORGANIZATION, SERVICE)
    configurer.configure_subscribers(subscribers, clear_subscriber_before=True, clear_store_before=True)


if __name__ == "__main__":
    configure()
