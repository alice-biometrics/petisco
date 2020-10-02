from petisco import RabbitMqConnector
from petisco.event.configurer.infrastructure.rabbitmq_configurer import (
    RabbitMqEventConfigurer,
)
from tests.modules.event.mothers.defaults import DEFAULT_ORGANIZATION, DEFAULT_SERVICE


class RabbitMqEventConfigurerMother:
    @staticmethod
    def default(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConfigurer(connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE)

    @staticmethod
    def with_ttl_10ms(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConfigurer(
            connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE, retry_ttl=10
        )

    @staticmethod
    def with_ttl_1s(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConfigurer(
            connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE, retry_ttl=1000
        )
