from __future__ import annotations

import os

from loguru import logger

from petisco.base.application.application_configurer import ApplicationConfigurer
from petisco.base.application.dependency_injection.container import Container
from petisco.base.application.notifier.notifier import Notifier
from petisco.base.application.notifier.notifier_exception_message import (
    NotifierExceptionMessage,
)
from petisco.base.domain.errors.unknown_error import UnknownError
from petisco.base.domain.message.command_bus import CommandBus
from petisco.base.domain.message.domain_event_bus import DomainEventBus
from petisco.base.domain.message.message_configurer import MessageConfigurer
from petisco.base.domain.message.message_consumer import MessageConsumer
from petisco.base.domain.message.message_subscriber import MessageSubscriber
from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_message_consumer import (
    RabbitMqMessageConsumer,
)

MAX_RETRIES = 5

CLEAR_SUBSCRIBER_BEFORE: bool = os.getenv(
    "PETISCO_RABBITMQ_CONFIGURER_CLEAR_SUBSCRIBER_BEFORE", "false"
).lower() in ["true", "1", "yes", "on"]
CLEAR_STORE_BEFORE: bool = os.getenv("PETISCO_RABBITMQ_CONFIGURER_CLEAR_STORE_BEFORE", "false").lower() in [
    "true",
    "1",
    "yes",
    "on",
]


class RabbitMqConfigurer(ApplicationConfigurer):
    def __init__(
        self,
        subscribers: list[type[MessageSubscriber]],
        execute_after_dependencies: bool = True,
        start_consuming: bool = True,
        alias: str | None = None,
        inner_bus_organization: str | None = None,
        inner_bus_service: str | None = None,
        clear_subscriber_before: bool | None = None,
        clear_store_before: bool | None = None,
        use_container_buses: bool = True,
    ):
        """
        Initializes an instance of RabbitMqConfigurer.

        Args:
            subscribers (list[MessageSubscriber]): A list of MessageSubscriber objects representing
                the message subscribers.
            execute_after_dependencies (bool, optional): Flag indicating whether to execute after
                dependencies. Defaults to True.
            start_consuming (bool, optional): Flag indicating whether to start consuming messages.
                Defaults to True.
            alias (str, optional): Alias for the MessageConfigurer and MessageConsumer
                (Container.get(MessageConfigurer|MessageConsumer, alias=self.alias)). Defaults to None.
            inner_bus_organization (str, optional): configured organization for inner buses (DomainEventBus
                and CommandBus). If None will configure consumer organization.
            inner_bus_service (str, optional): configured service for inner buses (DomainEventBus
                and CommandBus). If None will configure consumer service.
            use_container_buses (bool, optional): configure buses from petisco.Container.
        """
        self.subscribers = subscribers
        self.start_consuming = start_consuming
        self.alias = alias
        self.inner_bus_organization = inner_bus_organization
        self.inner_bus_service = inner_bus_service
        self.consumer: MessageConsumer | None = None
        self.clear_subscriber_before = (
            clear_subscriber_before if clear_subscriber_before else CLEAR_SUBSCRIBER_BEFORE
        )
        self.clear_store_before = clear_store_before if clear_store_before else CLEAR_STORE_BEFORE
        self.use_container_buses = use_container_buses

        super().__init__(execute_after_dependencies)

    def execute(self, testing: bool = False) -> None:
        configurer = Container.get(MessageConfigurer, alias=self.alias)
        try:
            configurer.configure_subscribers(
                self.subscribers,
                clear_subscriber_before=self.clear_subscriber_before,
                clear_store_before=self.clear_store_before,
            )

            if self.start_consuming:
                self.consumer = Container.get(MessageConsumer, alias=self.alias)

                if isinstance(self.consumer, RabbitMqMessageConsumer):
                    self.consumer.set_inner_bus_config(self.inner_bus_organization, self.inner_bus_service)
                    if self.use_container_buses is True:

                        def domain_event_bus_builder() -> DomainEventBus:
                            return Container.get(DomainEventBus)

                        def command_bus_builder() -> CommandBus:
                            return Container.get(CommandBus)

                        self.consumer.domain_event_bus_builder = domain_event_bus_builder
                        self.consumer.command_bus_builder = command_bus_builder

                self.consumer.add_subscribers(self.subscribers)
                self.consumer.start()
        except ConnectionError as ex:
            logger.error(f"Connection error with rabbit when trying to configure it. Message {str(ex)}")
            self.notify_connection_error(ex)

    def stop(self) -> None:
        if self.consumer:
            self.consumer.stop()

    def notify_connection_error(self, exception: Exception) -> None:
        notifier = Container.get(Notifier)
        error = UnknownError.from_exception(
            exception=exception,
            arguments={
                "service": self.inner_bus_service,
                "subscribers": self.subscribers,
            },
        )
        notifier_exception_message = NotifierExceptionMessage.from_unknown_error(
            error, title="Connection error trying to configure RabbitMQ"
        )
        notifier.publish_exception(notifier_exception_message)
