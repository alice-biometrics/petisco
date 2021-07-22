from typing import List, Type

import pytest
from meiga import BoolResult, isFailure, isSuccess
from meiga.assertions import assert_failure, assert_success

from petisco import Message, MessageSubscriber, PrintMiddleware
from tests.modules.base.mothers.message_mother import MessageMother


@pytest.mark.unit
def test_message_subscriber_should_construct_and_return_success_on_handle_method():
    class MyMessageSubscriber(MessageSubscriber):
        def subscribed_to(self) -> List[Type[Message]]:
            return [Message]

        def handle(self, message: Message) -> BoolResult:
            return isSuccess

    message_subscriber = MyMessageSubscriber()

    result = message_subscriber.handle(MessageMother.any())

    assert_success(result)


@pytest.mark.unit
def test_message_subscriber_should_construct_and_return_failure_on_handle_method():
    class MyMessageSubscriber(MessageSubscriber):
        def subscribed_to(self) -> List[Type[Message]]:
            return [Message]

        def handle(self, message: Message) -> BoolResult:
            return isFailure

    message_subscriber = MyMessageSubscriber()

    result = message_subscriber.handle(MessageMother.any())

    assert_failure(result)


@pytest.mark.unit
@pytest.mark.parametrize(
    "configured_middlewares",
    # [[], [PrintMiddleware], [PrintMiddleware, PrintMiddleware]],
    [[PrintMiddleware]],
)
def test_message_subscriber_should_create_command_input_and_output(
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

    assert_success(result)
