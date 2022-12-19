import pytest
from meiga import BoolResult, isSuccess

from petisco import Controller, PrintMiddleware
from tests.modules.base.application.middleware.configurable_middleware import (
    ConfigurableMiddleware,
)


@pytest.mark.unit
class TestMiddlewaresOnControllers:
    def should_use_config_middleware_with_non_configurable_middleware(self):
        class MyController(Controller):
            class Config:
                middlewares = [PrintMiddleware]

            def execute(self) -> BoolResult:
                return isSuccess

        controller = MyController()
        controller.execute()

    def should_use_config_middleware_with_a_configurable_middleware(self):
        class MyController(Controller):
            class Config:
                middlewares = [
                    ConfigurableMiddleware(
                        configurable_message_before="My Before Message",
                        configurable_message_after="My After Message",
                    )
                ]

            def execute(self) -> BoolResult:
                return isSuccess

        controller = MyController()
        controller.execute()

    def should_use_config_middleware_with_a_configurable_andother_non_configurable_middleware(
        self,
    ):
        class MyController(Controller):
            class Config:
                middlewares = [
                    PrintMiddleware,
                    ConfigurableMiddleware(
                        configurable_message_before="My Before Message",
                        configurable_message_after="My After Message",
                    ),
                ]

            def execute(self) -> BoolResult:
                return isSuccess

        controller = MyController()
        controller.execute()
