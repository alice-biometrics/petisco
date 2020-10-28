from petisco import RabbitMqConnector, RabbitMQEventPublisher
from tests.modules.event.mothers.defaults import DEFAULT_ORGANIZATION, DEFAULT_SERVICE


class RabbitMqEventPublisherMother:
    @staticmethod
    def default(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMQEventPublisher(
            connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE, f"{DEFAULT_SERVICE}-event"
        )
