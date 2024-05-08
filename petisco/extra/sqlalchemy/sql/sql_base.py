from __future__ import annotations

import inspect
from abc import abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T")


class SqlBase(DeclarativeBase, Generic[T]):
    def __repr__(self):
        attributes = ", ".join(
            f"{key}={value}" for key, value in self.__dict__.items() if not key.startswith("_")
        )
        return f"{self.__class__.__name__}({attributes})"

    def info(self) -> dict[str, str]:
        return {
            "name": self.__class__.__name__,
            "module": self.__class__.__module__,
            "file": inspect.getsourcefile(self.__class__),
        }

    @abstractmethod
    def to_domain(self) -> T:
        pass

    @staticmethod
    @abstractmethod
    def from_domain(domain_entity: T) -> SqlBase:
        pass
