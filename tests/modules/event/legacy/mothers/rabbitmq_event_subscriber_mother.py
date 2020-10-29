from typing import Callable

from petisco import RabbitMqConnector, ConfigEventSubscriber, RabbitMQEventSubscriber
from tests.modules.event.mothers.defaults import DEFAULT_ORGANIZATION, DEFAULT_SERVICE


class RabbitMqEventSubscriberMother:
    @staticmethod
    def default(main_handler: Callable, connector: RabbitMqConnector = None):
        connector = RabbitMqConnector() if not connector else connector
        return RabbitMQEventSubscriber(
            connector=connector,
            subscribers={
                "auth": ConfigEventSubscriber(
                    organization=DEFAULT_ORGANIZATION,
                    service=DEFAULT_SERVICE,
                    topic=f"{DEFAULT_SERVICE}-event",
                    handler=main_handler,
                )
            },
            connection_name="subscriber",
        )
