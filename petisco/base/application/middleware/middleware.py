from abc import ABC, abstractmethod
from typing import Any

from meiga import AnyResult


class Middleware(ABC):
    """
    A base class to model your Middleware.
    A Middleware works before some operations (Controller and Subscriber) and also before returning the final result.
    """

    wrapped_class_name: str = None
    wrapped_class_input_arguments: Any = None

    def set_data(
        self, wrapped_class_name: str, wrapped_class_input_arguments: Any
    ) -> None:
        self.wrapped_class_name = wrapped_class_name
        self.wrapped_class_input_arguments = wrapped_class_input_arguments

    @abstractmethod
    def before(self) -> None:
        pass

    @abstractmethod
    def after(self, result: AnyResult) -> None:
        pass
