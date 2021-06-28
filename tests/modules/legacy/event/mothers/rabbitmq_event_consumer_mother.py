from petisco.legacy import RabbitMqConnector

from petisco.legacy.logger.interface_logger import ILogger
from petisco.legacy.event.chaos.domain.interface_event_chaos import IEventChaos
from petisco.legacy.event.consumer.infrastructure.rabbitmq_event_consumer import (
    RabbitMqEventConsumer,
)
from petisco.legacy.logger.not_implemented_logger import NotImplementedLogger
from tests.modules.legacy.event.mothers.defaults import (
    DEFAULT_ORGANIZATION,
    DEFAULT_SERVICE,
    DEFAULT_MAX_RETRIES,
    DEFAULT_VERBOSE,
)


class RabbitMqEventConsumerMother:
    @staticmethod
    def default(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConsumer(
            connector,
            DEFAULT_ORGANIZATION,
            DEFAULT_SERVICE,
            DEFAULT_MAX_RETRIES,
            DEFAULT_VERBOSE,
        )

    @staticmethod
    def with_service(service: str, connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConsumer(
            connector,
            DEFAULT_ORGANIZATION,
            service,
            DEFAULT_MAX_RETRIES,
            DEFAULT_VERBOSE,
        )

    @staticmethod
    def with_max_retries(max_retries: int, connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConsumer(
            connector,
            DEFAULT_ORGANIZATION,
            DEFAULT_SERVICE,
            max_retries,
            DEFAULT_VERBOSE,
        )

    @staticmethod
    def without_retry(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConsumer(
            connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE, 0, DEFAULT_VERBOSE
        )

    @staticmethod
    def with_chaos(
        chaos: IEventChaos,
        max_retries: int,
        logger: ILogger = NotImplementedLogger(),
        connector: RabbitMqConnector = None,
    ):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConsumer(
            connector,
            DEFAULT_ORGANIZATION,
            DEFAULT_SERVICE,
            max_retries,
            DEFAULT_VERBOSE,
            chaos,
            logger,
        )