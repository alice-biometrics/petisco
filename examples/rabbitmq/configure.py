from examples.rabbitmq.common import ORGANIZATION, SERVICE, subscribers
from petisco.extra.rabbitmq import RabbitMqConnector, RabbitMqMessageConfigurer


def configure():
    connector = RabbitMqConnector()

    configurer = RabbitMqMessageConfigurer(
        ORGANIZATION,
        SERVICE,
        connector,
        # queue_config=QueueConfig(default_retry_ttl=RETRY_TTL),
    )
    configurer.configure_subscribers(subscribers)


if __name__ == "__main__":
    configure()
