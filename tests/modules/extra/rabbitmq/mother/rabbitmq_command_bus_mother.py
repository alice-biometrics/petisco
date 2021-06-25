from petisco.extra.rabbitmq import RabbitMqConnector, RabbitMqCommandBus
from tests.modules.base.mothers.message_meta_mother import MessageMetaMother
from tests.modules.extra.rabbitmq.mother.defaults import (
    DEFAULT_ORGANIZATION,
    DEFAULT_SERVICE,
)


class RabbitMqCommandBusMother:
    @staticmethod
    def default(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqCommandBus(connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE)

    @staticmethod
    def with_service(service: str, connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqCommandBus(connector, DEFAULT_ORGANIZATION, service)

    @staticmethod
    def with_info_id(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqCommandBus(
            connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE
        ).with_meta(MessageMetaMother.with_meta_with_info())
