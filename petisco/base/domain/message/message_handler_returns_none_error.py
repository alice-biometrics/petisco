from __future__ import annotations

from typing import Callable

from meiga import BoolResult

from petisco.base.domain.message.message import Message


class MessageHandlerReturnsNoneError(ValueError):
    def __init__(self, handler: Callable[[Message], BoolResult]):
        handler_name = getattr(handler, "__name__", repr(handler))
        handler_module = handler.__module__ + "."
        message = f"Subscribers (event handlers) must return a Result object. Please check {handler_module}{handler_name}"
        super().__init__(message)
