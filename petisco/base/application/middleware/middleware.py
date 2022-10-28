from abc import ABC, abstractmethod
from typing import Any

from meiga import AnyResult


class Middleware(ABC):
    def __init__(
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
