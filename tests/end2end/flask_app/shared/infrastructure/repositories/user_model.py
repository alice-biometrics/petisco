from sqlalchemy import Column, Integer, String

from petisco.persistence.persistence import Persistence

Base = Persistence.get_base("petisco-sql")


class UserModel(Base):
    __tablename__ = "User"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", String(12))
    client_id = Column("client_id", String(50))
    name = Column("name", String(50))
