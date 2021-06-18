from petisco.extra.rabbitmq import (
    RabbitMqConnector,
    RabbitMqMessageConfigurer,
    QueueConfig,
)
from tests.modules.extra.rabbitmq.mother.defaults import (
    DEFAULT_ORGANIZATION,
    DEFAULT_SERVICE,
)


class RabbitMqMessageConfigurerMother:
    @staticmethod
    def default(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqMessageConfigurer(
            connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE
        )

    @staticmethod
    def with_retry_ttl_10ms(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqMessageConfigurer(
            connector,
            DEFAULT_ORGANIZATION,
            DEFAULT_SERVICE,
            QueueConfig.default(default_retry_ttl=10),
        )

    @staticmethod
    def with_main_and_retry_ttl_10ms(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqMessageConfigurer(
            connector,
            DEFAULT_ORGANIZATION,
            DEFAULT_SERVICE,
            QueueConfig.default(default_retry_ttl=10, default_main_ttl=10),
        )

    @staticmethod
    def with_main_and_retry_ttl_100ms(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqMessageConfigurer(
            connector,
            DEFAULT_ORGANIZATION,
            DEFAULT_SERVICE,
            QueueConfig.default(default_retry_ttl=100, default_main_ttl=100),
        )

    @staticmethod
    def with_service(service: str, connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqMessageConfigurer(
            connector,
            DEFAULT_ORGANIZATION,
            service,
            QueueConfig.default(default_retry_ttl=10),
        )

    @staticmethod
    def with_ttl_1s(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqMessageConfigurer(
            connector,
            DEFAULT_ORGANIZATION,
            DEFAULT_SERVICE,
            QueueConfig.default(default_retry_ttl=1000),
        )

    @staticmethod
    def with_queue_config(
        queue_config: QueueConfig, connector: RabbitMqConnector = None
    ):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqMessageConfigurer(
            connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE, queue_config
        )
