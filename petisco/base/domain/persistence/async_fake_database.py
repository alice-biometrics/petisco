from __future__ import annotations

from typing import Any, Callable, ContextManager

from petisco.base.domain.persistence.async_database import AsyncDatabase
from petisco.base.domain.persistence.database import T


class AsyncFakeDatabase(AsyncDatabase):
    def initialize(self, *args: Any, **kwargs: Any) -> None:
        pass

    def delete(self) -> None:
        pass

    def clear_data(self) -> None:
        pass

    async def is_available(self) -> bool:
        pass

    def get_session_scope(self) -> Callable[..., ContextManager[T]]:
        pass
