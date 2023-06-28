import inspect
from abc import abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped


class User(BaseModel):
    name: str
    age: int | None


T = TypeVar("T")


class AlternativeSqlBase(DeclarativeBase, Generic[T]):
    def __repr__(self) -> str:
        attributes = ", ".join(
            f"{key}={value}"
            for key, value in self.__dict__.items()
            if not key.startswith("_")
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
    def from_domain(domain_entity: T) -> "AlternativeSqlBase":
        pass


class Profession(BaseModel):
    name: str
    salary: int


class SqlProfession(AlternativeSqlBase[Profession]):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(30))
    salary: Mapped[int] = Column(Integer)

    def to_domain(self) -> Profession:
        return Profession(name=self.name, salary=self.salary)

    @staticmethod
    def from_domain(domain_entity: User) -> "SqlProfession":
        return SqlProfession(name=domain_entity.name, salary=domain_entity.salary)
