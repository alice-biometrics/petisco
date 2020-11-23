from petisco import RabbitMqConnector
from petisco.event.bus.infrastructure.rabbitmq_event_bus import RabbitMqEventBus
from tests.modules.event.mothers.defaults import DEFAULT_ORGANIZATION, DEFAULT_SERVICE
from tests.modules.shared.info_id_mother import InfoIdMother


class RabbitMqEventBusMother:
    @staticmethod
    def default(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventBus(connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE)

    @staticmethod
    def with_service(service: str, connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventBus(connector, DEFAULT_ORGANIZATION, service)

    @staticmethod
    def with_info_id(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqEventBus(
            connector, DEFAULT_ORGANIZATION, DEFAULT_SERVICE
        ).with_info_id(InfoIdMother.random())
