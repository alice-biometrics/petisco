from typing import Union

from petisco import DomainEventBus, NotImplementedDomainEventBus
from petisco.extra.rabbitmq import RabbitMqConnector, RabbitMqDomainEventBus
from tests.modules.base.mothers.message_meta_mother import MessageMetaMother
from tests.modules.extra.rabbitmq.mother.defaults import (
    DEFAULT_ORGANIZATION,
    DEFAULT_SERVICE,
)


class RabbitMqDomainEventBusMother:
    @staticmethod
    def default(connector: RabbitMqConnector = None, fallback: Union[DomainEventBus, None] = NotImplementedDomainEventBus()):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqDomainEventBus(DEFAULT_ORGANIZATION, DEFAULT_SERVICE, connector, fallback=fallback)

    @staticmethod
    def with_service(service: str, connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqDomainEventBus(DEFAULT_ORGANIZATION, service, connector)

    @staticmethod
    def with_info_id(connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMqDomainEventBus(
            DEFAULT_ORGANIZATION, DEFAULT_SERVICE, connector
        ).with_meta(MessageMetaMother.with_meta_with_info())
