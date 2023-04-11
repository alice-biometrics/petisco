from petisco.base.domain.message.chaos.message_chaos import MessageChaos
from petisco.extra.rabbitmq import RabbitMqConnector, RabbitMqMessageConsumer
from petisco.legacy.logger.interface_logger import ILogger
from petisco.legacy.logger.not_implemented_logger import NotImplementedLogger
from tests.modules.extra.rabbitmq.mother.defaults import (
    DEFAULT_MAX_RETRIES,
    DEFAULT_ORGANIZATION,
    DEFAULT_SERVICE,
    DEFAULT_VERBOSE,
)


class RabbitMqMessageConsumerMother:
    @staticmethod
    def default(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqMessageConsumer(
            DEFAULT_ORGANIZATION,
            DEFAULT_SERVICE,
            DEFAULT_MAX_RETRIES,
            connector,
            DEFAULT_VERBOSE,
        )

    @staticmethod
    def with_service(service: str, connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqMessageConsumer(
            DEFAULT_ORGANIZATION,
            service,
            DEFAULT_MAX_RETRIES,
            connector,
            DEFAULT_VERBOSE,
        )

    @staticmethod
    def with_max_retries(max_retries: int, connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqMessageConsumer(
            DEFAULT_ORGANIZATION,
            DEFAULT_SERVICE,
            max_retries,
            connector,
            DEFAULT_VERBOSE,
        )

    @staticmethod
    def without_retry(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqMessageConsumer(
            DEFAULT_ORGANIZATION, DEFAULT_SERVICE, 0, connector, DEFAULT_VERBOSE
        )

    @staticmethod
    def with_chaos(
        chaos: MessageChaos,
        max_retries: int,
        logger: ILogger = NotImplementedLogger(),
        connector: RabbitMqConnector = None,
    ):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqMessageConsumer(
            DEFAULT_ORGANIZATION,
            DEFAULT_SERVICE,
            max_retries,
            connector,
            DEFAULT_VERBOSE,
            chaos,
            logger,
        )

    @staticmethod
    def with_rabbitmq_key_prefix(
        rabbitmq_key_prefix: str, connector: RabbitMqConnector = None
    ):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqMessageConsumer(
            DEFAULT_ORGANIZATION,
            DEFAULT_SERVICE,
            DEFAULT_MAX_RETRIES,
            connector,
            DEFAULT_VERBOSE,
            rabbitmq_key_prefix=rabbitmq_key_prefix,
        )
