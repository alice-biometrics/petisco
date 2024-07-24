from playground.rabbitmq_consumers.common import ORGANIZATION, SERVICE, subscribers

from petisco.extra.rabbitmq import RabbitMqConnector, RabbitMqMessageConfigurer


def configure() -> None:
    connector = RabbitMqConnector()

    configurer = RabbitMqMessageConfigurer(
        ORGANIZATION,
        SERVICE,
        connector,
        # queue_config=QueueConfig(default_retry_ttl=RETRY_TTL),
    )
    configurer.clear_subscribers(subscribers)


if __name__ == "__main__":
    configure()
