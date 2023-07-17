from __future__ import annotations

import os

from petisco.base.application.application_configurer import ApplicationConfigurer
from petisco.base.application.dependency_injection.container import Container
from petisco.base.domain.message.message_configurer import MessageConfigurer
from petisco.base.domain.message.message_consumer import MessageConsumer
from petisco.base.domain.message.message_subscriber import MessageSubscriber

MAX_RETRIES = 5

CLEAR_SUBSCRIBER_BEFORE: bool = os.getenv(
    "PETISCO_RABBITMQ_CONFIGURER_CLEAR_SUBSCRIBER_BEFORE", "false"
).lower() in ["true", "1", "yes", "on"]
CLEAR_STORE_BEFORE: bool = os.getenv(
    "PETISCO_RABBITMQ_CONFIGURER_CLEAR_STORE_BEFORE", "false"
).lower() in ["true", "1", "yes", "on"]


class RabbitMqConfigurer(ApplicationConfigurer):
    def __init__(
        self,
        subscribers: list[type[MessageSubscriber]],
        execute_after_dependencies: bool = True,
        start_consuming: bool = True,
        alias: str = None,
    ):
        """
        Initializes an instance of RabbitMqConfigurer.

        Args:
            subscribers (list[MessageSubscriber]): A list of MessageSubscriber objects representing the message subscribers.
            execute_after_dependencies (bool, optional): Flag indicating whether to execute after dependencies. Defaults to True.
            start_consuming (bool, optional): Flag indicating whether to start consuming messages. Defaults to True.
            alias (str, optional): Alias for the MessageConfigurer and MessageConsumer (Container.get(MessageConfigurer|MessageConsumer, alias=self.alias)). Defaults to None.
        """
        self.subscribers = subscribers
        self.start_consuming = start_consuming
        self.alias = alias
        super().__init__(execute_after_dependencies)

    def execute(self, testing: bool = False) -> None:
        configurer = Container.get(MessageConfigurer, alias=self.alias)
        configurer.configure_subscribers(
            self.subscribers,
            clear_subscriber_before=CLEAR_SUBSCRIBER_BEFORE,
            clear_store_before=CLEAR_STORE_BEFORE,
        )

        if self.start_consuming:
            consumer = Container.get(MessageConsumer, alias=self.alias)
            consumer.add_subscribers(self.subscribers)
            consumer.start()
