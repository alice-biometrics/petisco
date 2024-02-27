from typing import Any

import pytest
from meiga import AnyResult, isSuccess

from petisco import Controller, MessageSubscriber, Middleware, MiddlewareScope


class AllScopeMiddleware(Middleware):
    before_is_executed = False
    after_is_executed = False

    def before(self) -> None:
        self.before_is_executed = True

    def after(self, result: AnyResult) -> None:
        self.after_is_executed = True


class OnlyControllerMiddleware(Middleware):
    scope = MiddlewareScope.CONTROLLER
    before_is_executed = False
    after_is_executed = False

    def before(self) -> None:
        self.before_is_executed = True

    def after(self, result: AnyResult) -> None:
        self.after_is_executed = True


class OnlySubscriberMiddleware(Middleware):
    scope = MiddlewareScope.SUBSCRIBER
    before_is_executed = False
    after_is_executed = False

    def before(self) -> None:
        self.before_is_executed = True

    def after(self, result: AnyResult) -> None:
        self.after_is_executed = True


@pytest.mark.unit
class TestScopeMiddleware:
    @pytest.mark.parametrize(
        "middleware", [AllScopeMiddleware, OnlySubscriberMiddleware]
    )
    def should_execute_middleware_when_is_subscriber_when_subscribed_is_in_scope(
        self, middleware
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

        assert subscriber.Config.middlewares[0].before_is_executed is True
        assert subscriber.Config.middlewares[0].after_is_executed is True

    @pytest.mark.parametrize(
        "middleware", [AllScopeMiddleware, OnlyControllerMiddleware]
    )
    def should_execute_middleware_when_is_controller_when_subscribed_is_in_scope(
        self, middleware
    ) -> None:
        class MyController(Controller):
            class Config:
                middlewares = [middleware]

            def execute(self) -> Any:
                return isSuccess

        controller = MyController()
        result = controller.execute()
        result.assert_success()

        assert controller.Config.middlewares[0].before_is_executed is True
        assert controller.Config.middlewares[0].after_is_executed is True

    def should_skip_middleware_when_is_subscriber_when_only_controller_middleware(
        self,
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

        assert subscriber.Config.middlewares[0].before_is_executed is False
        assert subscriber.Config.middlewares[0].after_is_executed is False

    def should_skip_middleware_when_is_controller_when_only_subscriber_middleware(
        self,
    ) -> None:
        class MyController(Controller):
            class Config:
                middlewares = [OnlySubscriberMiddleware]

            def execute(self) -> Any:
                return isSuccess

        controller = MyController()
        result = controller.execute()
        result.assert_success()

        assert controller.Config.middlewares[0].before_is_executed is False
        assert controller.Config.middlewares[0].after_is_executed is False
