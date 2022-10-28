import os
from distutils.util import strtobool
from typing import List, Optional

from petisco.base.application.application_configurer import ApplicationConfigurer
from petisco.base.application.dependency_injection.container import Container
from petisco.base.domain.message.message_subscriber import MessageSubscriber

MAX_RETRIES = 5

CLEAR_SUBSCRIBER_BEFORE = strtobool(
    os.getenv("PETISCO_RABBITMQ_CONFIGURER_CLEAR_SUBSCRIBER_BEFORE", "false")
)
CLEAR_STORE_BEFORE = strtobool(
    os.getenv("PETISCO_RABBITMQ_CONFIGURER_CLEAR_STORE_BEFORE", "false")
)


class RabbitMqMessageApplicationConfigurer(ApplicationConfigurer):
    def __init__(
        self,
        execute_after_dependencies: bool = True,
        subscribers: Optional[List[MessageSubscriber]] = None,
    ):
        self.execute_after_dependencies = execute_after_dependencies
        self.subscribers = subscribers
        super().__init__(execute_after_dependencies)

    def execute(self, testing: bool = False) -> None:
        configurer = Container.get("message_configurer")
        configurer.configure_subscribers(
            self.subscribers,
            clear_subscriber_before=CLEAR_SUBSCRIBER_BEFORE,
            clear_store_before=CLEAR_STORE_BEFORE,
        )
