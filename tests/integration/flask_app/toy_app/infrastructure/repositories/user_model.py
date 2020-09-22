from sqlalchemy import Column, Integer, String
from petisco.persistence.sqlalchemy.sqlalchemy_persistence import SqlAlchemyPersistence

Base = SqlAlchemyPersistence.get_instance().sources["petisco"]["base"]


class UserModel(Base):
    __tablename__ = "User"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", String(12))
    client_id = Column("client_id", String(50))
    name = Column("name", String(50))
