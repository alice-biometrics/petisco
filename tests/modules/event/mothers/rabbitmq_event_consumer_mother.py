from petisco import RabbitMqConnector
from petisco.event.consumer.infrastructure.rabbitmq_event_comsumer import (
    RabbitMqEventConsumer,
)
from tests.modules.event.mothers.defaults import (
    DEFAULT_ORGANIZATION,
    DEFAULT_SERVICE,
    DEFAULT_MAX_RETRIES,
)


class RabbitMqEventConsumerMother:
    @staticmethod
    def default(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConsumer(
            connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE, DEFAULT_MAX_RETRIES
        )

    @staticmethod
    def with_max_retries(max_retries: int, connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventConsumer(
            connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE, max_retries
        )
