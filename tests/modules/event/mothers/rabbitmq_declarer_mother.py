from petisco import RabbitMqConnector
from petisco.event.configurer.infrastructure.rabbitmq_declarer import RabbitMqDeclarer

from tests.modules.event.mothers.defaults import DEFAULT_ORGANIZATION, DEFAULT_SERVICE


class RabbitMqDeclarerMother:
    @staticmethod
    def default(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqDeclarer(
            connector=connector,
            channel_name=f"{DEFAULT_ORGANIZATION}.{DEFAULT_SERVICE}",
        )
