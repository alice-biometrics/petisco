from typing import Union

from petisco import CommandBus
from petisco.extra.rabbitmq import RabbitMqCommandBus, RabbitMqConnector
from tests.modules.base.mothers.message_meta_mother import MessageMetaMother
from tests.modules.extra.rabbitmq.mother.defaults import (
    DEFAULT_ORGANIZATION,
    DEFAULT_SERVICE,
)


class RabbitMqCommandBusMother:
    @staticmethod
    def default(
        connector: RabbitMqConnector = None,
        fallback: Union[CommandBus, None] = None,
    ):
        connector = connector if connector else RabbitMqConnector()
        return RabbitMqCommandBus(DEFAULT_ORGANIZATION, DEFAULT_SERVICE, connector, fallback=fallback)

    @staticmethod
    def with_service(service: str, connector: RabbitMqConnector = None):
        connector = connector if connector else RabbitMqConnector()
        return RabbitMqCommandBus(DEFAULT_ORGANIZATION, service, connector)

    @staticmethod
    def with_info_id(connector: RabbitMqConnector = None):
        connector = connector if connector else RabbitMqConnector()
        return RabbitMqCommandBus(DEFAULT_ORGANIZATION, DEFAULT_SERVICE, connector).with_meta(
            MessageMetaMother.with_meta_with_info()
        )
