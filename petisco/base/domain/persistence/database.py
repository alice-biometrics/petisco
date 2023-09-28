from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, ContextManager, Generic, TypeVar

T = TypeVar("T")


class Database(Generic[T], ABC):
    alias: str | None = None

    def __init__(self, alias: str | None = None):
        self.alias = alias

    def get_key(self) -> str:
        return type(self).__name__ if not self.alias else self.alias

    def info(self) -> dict[str, Any]:
        return {"type": self.__class__.__name__, "alias": self.alias}

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
