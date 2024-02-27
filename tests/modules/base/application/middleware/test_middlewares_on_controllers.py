from typing import List

import pytest
from meiga import BoolResult, isSuccess

from petisco import Controller, Middleware, PrintMiddleware
from petisco.base.application.application_info import ApplicationInfo
from tests.modules.base.application.middleware.configurable_middleware import (
    ConfigurableMiddleware,
)


@pytest.mark.unit
class TestMiddlewaresOnControllers:
    def tear_down(self):
        self.set_application_info_with_middlewares([])

    def set_application_info_with_middlewares(self, middlewares: List[Middleware]):
        ApplicationInfo(
            name=ApplicationInfo().name,
            organization=ApplicationInfo().organization,
            version=ApplicationInfo().version,
            deployed_at=ApplicationInfo().deployed_at,
            shared_error_map=ApplicationInfo().shared_error_map,
            shared_middlewares=middlewares,
            force_recreation=True,
        )

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

    def should_use_config_middleware_with_a_configurable_and_other_non_configurable_middleware(
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

    def should_use_config_without_global_middlewares(
        self,
    ):
        self.set_application_info_with_middlewares([PrintMiddleware])

        class MyController(Controller):
            class Config:
                middlewares = []
                use_global_middlewares = False

            def execute(self) -> BoolResult:
                return isSuccess

        controller = MyController()
        controller.execute()

    def should_use_config_with_global_middlewares(
        self,
    ):
        self.set_application_info_with_middlewares([PrintMiddleware])

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
