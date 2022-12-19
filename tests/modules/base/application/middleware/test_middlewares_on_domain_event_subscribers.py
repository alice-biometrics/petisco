from typing import List, Type

import pytest
from meiga import BoolResult, isSuccess

from petisco import DomainEvent, DomainEventSubscriber, PrintMiddleware
from tests.modules.base.application.middleware.configurable_middleware import (
    ConfigurableMiddleware,
)


class UserCreated(DomainEvent):
    pass


@pytest.mark.unit
class TestMiddlewaresOnDomainEventSubscribers:
    def should_use_config_middleware_with_non_configurable_middleware(self):
        class MyDomainEventSubscriber(DomainEventSubscriber):
            class Config:
                middlewares = [PrintMiddleware]

            def subscribed_to(self) -> List[Type[DomainEvent]]:
                return [UserCreated]

            def handle(self, domain_event: DomainEvent) -> BoolResult:
                return isSuccess

        subscriber = MyDomainEventSubscriber()
        subscriber.handle(UserCreated())

    def should_use_config_middleware_with_a_configurable_middleware(self):
        class MyDomainEventSubscriber(DomainEventSubscriber):
            class Config:
                middlewares = [
                    ConfigurableMiddleware(
                        configurable_message_before="My Before Message",
                        configurable_message_after="My After Message",
                    )
                ]

            def subscribed_to(self) -> List[Type[DomainEvent]]:
                return [UserCreated]

            def handle(self, domain_event: DomainEvent) -> BoolResult:
                return isSuccess

        subscriber = MyDomainEventSubscriber()
        subscriber.handle(UserCreated())

    def should_use_config_middleware_with_a_configurable_andother_non_configurable_middleware(
        self,
    ):
        class MyDomainEventSubscriber(DomainEventSubscriber):
            class Config:
                middlewares = [
                    PrintMiddleware,
                    ConfigurableMiddleware(
                        configurable_message_before="My Before Message",
                        configurable_message_after="My After Message",
                    ),
                ]

            def subscribed_to(self) -> List[Type[DomainEvent]]:
                return [UserCreated]

            def handle(self, domain_event: DomainEvent) -> BoolResult:
                return isSuccess

        subscriber = MyDomainEventSubscriber()
        subscriber.handle(UserCreated())
