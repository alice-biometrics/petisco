from typing import List, Type

import pytest
from meiga import AnyResult, BoolResult, isFailure, isSuccess

from petisco import Message, MessageSubscriber, Middleware, PrintMiddleware
from tests.modules.base.mothers.message_mother import MessageMother


@pytest.mark.unit
class TestMessageSubscriber:
    def should_construct_and_return_success_on_handle_method(self):  # noqa
        class MyMessageSubscriber(MessageSubscriber):
            def subscribed_to(self) -> List[Type[Message]]:
                return [Message]

            def handle(self, message: Message) -> BoolResult:
                return isSuccess

        message_subscriber = MyMessageSubscriber()

        result = message_subscriber.handle(MessageMother.any())

        result.assert_success()

    def should_construct_and_return_failure_on_handle_method(self):  # noqa
        class MyMessageSubscriber(MessageSubscriber):
            def subscribed_to(self) -> List[Type[Message]]:
                return [Message]

            def handle(self, message: Message) -> BoolResult:
                return isFailure

        message_subscriber = MyMessageSubscriber()

        result = message_subscriber.handle(MessageMother.any())

        result.assert_failure()

    @pytest.mark.parametrize(
        "configured_middlewares",
        [[PrintMiddleware]],
    )
    def should_create_command_input_and_output(
        self,
        configured_middlewares,
    ):
        class MyMessageSubscriber(MessageSubscriber):
            class Config:
                middlewares = configured_middlewares

            def subscribed_to(self) -> List[Type[Message]]:
                return [Message]

            def handle(self, message: Message) -> BoolResult:
                return isSuccess

        message_subscriber = MyMessageSubscriber()

        result = message_subscriber.handle(MessageMother.any())

        result.assert_success()

    def should_not_fail_when_middleware_raise_unexpected_error_on_before(self):  # noqa
        class RaiseErrorOnBeforeMiddleware(Middleware):
            def before(self) -> None:
                raise RuntimeError("Error in before")

            def after(self, result: AnyResult) -> None:
                pass

        class MyMessageSubscriber(MessageSubscriber):
            class Config:
                middlewares = [RaiseErrorOnBeforeMiddleware]

            def subscribed_to(self) -> List[Type[Message]]:
                return [Message]

            def handle(self, message: Message) -> BoolResult:
                return isSuccess

        message_subscriber = MyMessageSubscriber()

        result = message_subscriber.handle(MessageMother.any())

        result.assert_success()

    def should_not_fail_when_middleware_raise_unexpected_error_on_after(self):  # noqa
        class RaiseErrorOnAfterMiddleware(Middleware):
            def before(self) -> None:
                pass

            def after(self, result: AnyResult) -> None:
                raise RuntimeError("Error in after")

        class MyMessageSubscriber(MessageSubscriber):
            class Config:
                middlewares = [RaiseErrorOnAfterMiddleware]

            def subscribed_to(self) -> List[Type[Message]]:
                return [Message]

            def handle(self, message: Message) -> BoolResult:
                return isSuccess

        message_subscriber = MyMessageSubscriber()

        result = message_subscriber.handle(MessageMother.any())

        result.assert_success()
