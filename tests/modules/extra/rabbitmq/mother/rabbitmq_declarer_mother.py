from petisco.extra.rabbitmq import RabbitMqConnector, RabbitMqDeclarer
from tests.modules.extra.rabbitmq.mother.defaults import (
    DEFAULT_ORGANIZATION,
    DEFAULT_SERVICE,
)


class RabbitMqDeclarerMother:
    @staticmethod
    def default(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqDeclarer(
            connector=connector,
            channel_name=f"{DEFAULT_ORGANIZATION}.{DEFAULT_SERVICE}",
        )
