from petisco import RabbitMqConnector
from petisco.event.configurer.infrastructure.rabbitmq_event_configurer import (
    RabbitMqEventConfigurer,
)
from tests.modules.event.mothers.defaults import DEFAULT_ORGANIZATION, DEFAULT_SERVICE


class RabbitMqEventConfigurerMother:
    @staticmethod
    def default(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConfigurer(connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE)

    @staticmethod
    def with_retry_ttl_10ms(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConfigurer(
            connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE, retry_ttl=10
        )

    @staticmethod
    def with_main_and_retry_ttl_10ms(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConfigurer(
            connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE, retry_ttl=10, main_ttl=10
        )

    @staticmethod
    def with_main_and_retry_ttl_100ms(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConfigurer(
            connector,
            DEFAULT_ORGANIZATION,
            DEFAULT_SERVICE,
            retry_ttl=100,
            main_ttl=100,
        )

    @staticmethod
    def with_service(service: str, connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConfigurer(
            connector, DEFAULT_ORGANIZATION, service, retry_ttl=10
        )

    @staticmethod
    def with_ttl_1s(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConfigurer(
            connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE, retry_ttl=1000
        )
