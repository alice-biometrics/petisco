from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped

from petisco.extra.sqlalchemy import SqlBase


class User(BaseModel):
    name: str
    age: int | None


class SqlUser(SqlBase[User]):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(30))
    age: Mapped[int] = Column(Integer)

    def to_domain(self) -> User:
        return User(name=self.name, age=self.age)

    @staticmethod
    def from_domain(domain_entity: User) -> "SqlUser":
        return SqlUser(name=domain_entity.name, age=domain_entity.age)
