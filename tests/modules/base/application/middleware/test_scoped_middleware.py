from typing import Any
from unittest import mock
from unittest.mock import Mock

import pytest
from meiga import AnyResult, isSuccess

from petisco import (
    Controller,
    DomainEvent,
    DomainEventBus,
    MessageSubscriber,
    Middleware,
    MiddlewareScope,
    NotImplementedDomainEventBus,
)


class MyDomainEvent(DomainEvent):
    pass


class TestScopeMiddleware(Middleware):
    def __init__(self) -> None:
        self.event_bus: DomainEventBus = NotImplementedDomainEventBus()

    def before(self) -> None:
        self.event_bus.publish(MyDomainEvent)

    def after(self, result: AnyResult) -> None:
        self.event_bus.publish(MyDomainEvent)


class AllScopeMiddleware(TestScopeMiddleware):
    pass


class OnlyControllerMiddleware(TestScopeMiddleware):
    scope = MiddlewareScope.CONTROLLER


class OnlySubscriberMiddleware(TestScopeMiddleware):
    scope = MiddlewareScope.SUBSCRIBER


@pytest.mark.unit
class TestScopeMiddleware:
    @pytest.mark.parametrize(
        "middleware", [AllScopeMiddleware, OnlySubscriberMiddleware]
    )
    @mock.patch("petisco.NotImplementedDomainEventBus.publish")
    def should_execute_middleware_when_is_subscriber_when_subscribed_is_in_scope(
        self, mock_event_bus: Mock, middleware
    ) -> None:
        class MySubscriber(MessageSubscriber):
            class Config:
                middlewares = [middleware]

            def subscribed_to(self) -> Any:
                pass

            def handle(self, message: Any) -> Any:
                return isSuccess

        subscriber = MySubscriber()
        result = subscriber.handle("")
        result.assert_success()

        assert mock_event_bus.call_count == 2

    @pytest.mark.parametrize(
        "middleware", [AllScopeMiddleware, OnlyControllerMiddleware]
    )
    @mock.patch("petisco.NotImplementedDomainEventBus.publish")
    def should_execute_middleware_when_is_controller_when_subscribed_is_in_scope(
        self, mock_event_bus: Mock, middleware
    ) -> None:
        class MyController(Controller):
            class Config:
                middlewares = [middleware]

            def execute(self) -> Any:
                return isSuccess

        controller = MyController()
        result = controller.execute()
        result.assert_success()

        assert mock_event_bus.call_count == 2

    @mock.patch("petisco.NotImplementedDomainEventBus.publish")
    def should_skip_middleware_when_is_subscriber_when_only_controller_middleware(
        self,
        mock_event_bus: Mock,
    ) -> None:
        class MySubscriber(MessageSubscriber):
            class Config:
                middlewares = [OnlyControllerMiddleware]

            def subscribed_to(self) -> Any:
                pass

            def handle(self, message: Any) -> Any:
                return isSuccess

        subscriber = MySubscriber()
        result = subscriber.handle("")
        result.assert_success()

        mock_event_bus.assert_not_called()

    @mock.patch("petisco.NotImplementedDomainEventBus.publish")
    def should_skip_middleware_when_is_controller_when_only_subscriber_middleware(
        self,
        mock_event_bus: Mock,
    ) -> None:
        class MyController(Controller):
            class Config:
                middlewares = [OnlySubscriberMiddleware]

            def execute(self) -> Any:
                return isSuccess

        controller = MyController()
        result = controller.execute()
        result.assert_success()

        mock_event_bus.assert_not_called()
