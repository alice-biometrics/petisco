from typing import Callable


class MessageHandlerReturnsNoneError(ValueError):
    def __init__(self, handler: Callable):
        handler_name = getattr(handler, "__name__", repr(handler))
        handler_module = getattr(handler, "__module__") + "."
        message = f"Subscribers (event handlers) must return a Result object. Please check {handler_module}{handler_name}"
        super().__init__(message)
