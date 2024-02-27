from typing import Any

import pytest
from meiga import AnyResult, isSuccess

from petisco import Controller, MessageSubscriber, Middleware


class InvalidMiddleware(Middleware):
    def __init__(self, my_fancy_parameter: str):
        self.my_fancy_parameter = my_fancy_parameter

    def before(self) -> None:
        pass

    def after(self, result: AnyResult) -> None:
        pass


@pytest.mark.unit
class TestInvalidMiddleware:
    def should_fail_on_controller_when_invalid_middleware_is_defined(
        self,
    ) -> None:
        class MyController(Controller):
            class Config:
                middlewares = [InvalidMiddleware]

            def execute(self) -> Any:
                return isSuccess

        with pytest.raises(TypeError):
            MyController().execute()

    def should_fail_on_subscriber_when_invalid_middleware_is_defined(
        self,
    ) -> None:
        class MySubscriber(MessageSubscriber):
            class Config:
                middlewares = [InvalidMiddleware]

            def subscribed_to(self) -> Any:
                pass

            def handle(self, message: Any) -> Any:
                return isSuccess

        with pytest.raises(TypeError):
            MySubscriber().handle("")
