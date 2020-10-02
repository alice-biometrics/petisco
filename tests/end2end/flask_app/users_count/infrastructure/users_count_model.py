from sqlalchemy import Column, Integer
from petisco.persistence.sqlalchemy.sqlalchemy_persistence import SqlAlchemyPersistence


Base = SqlAlchemyPersistence.get_instance().sources["petisco"]["base"]


class UsersCountModel(Base):
    __tablename__ = "UsersCount"

    count = Column("count", Integer, primary_key=True)
