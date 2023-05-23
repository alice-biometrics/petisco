from __future__ import annotations

from abc import abstractmethod
from typing import Generic, TypeVar

from petisco.base.domain.persistence.database import Database

T = TypeVar("T")


class AsyncDatabase(Generic[T], Database[T]):
    @abstractmethod
    async def is_available(self) -> bool:
        raise NotImplementedError
