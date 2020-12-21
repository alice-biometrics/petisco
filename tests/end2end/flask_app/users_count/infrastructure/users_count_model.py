from sqlalchemy import Column, Integer

from petisco.persistence.persistence import Persistence

Base = Persistence.get_base("petisco-sql")


class UsersCountModel(Base):
    __tablename__ = "UsersCount"

    count = Column("count", Integer, primary_key=True)
