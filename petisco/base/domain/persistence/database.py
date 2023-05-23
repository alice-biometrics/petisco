from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, ContextManager, Generic, TypeVar

T = TypeVar("T")


class Database(Generic[T], ABC):
    def __init__(self, name: str):
        self.name = name

    def info(self) -> dict[str, Any]:
        return {"name": self.name}

    @abstractmethod
    def initialize(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def clear_data(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_available(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_session_scope(self) -> Callable[..., ContextManager[T]]:
        raise NotImplementedError
