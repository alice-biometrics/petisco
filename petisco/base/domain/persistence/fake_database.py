from __future__ import annotations

from typing import Any, Callable, ContextManager

from petisco.base.domain.persistence.database import Database, T


class FakeDatabase(Database):
    def initialize(self, *args: Any, **kwargs: Any) -> None:
        pass

    def delete(self) -> None:
        pass

    def clear_data(self) -> None:
        pass

    def is_available(self) -> bool:
        pass

    def get_session_scope(self) -> Callable[..., ContextManager[T]]:
        pass
