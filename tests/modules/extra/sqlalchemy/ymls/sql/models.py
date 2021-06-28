from sqlalchemy import String, Integer, Column, Float, ForeignKey

from petisco.base.domain.persistence.persistence import Persistence

try:
    Base = Persistence.get_base("mysql_test")
except IndexError:
    Base = Persistence.get_base("sqlite_test")


class ClientModel(Base):
    __tablename__ = "Client"

    id = Column(Integer, primary_key=True)
    client_id = Column(String(36))
    name = Column(String(100), nullable=False)


class UserModel(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(36))
    name = Column(String(100), nullable=False)
    client_id = Column(Integer, ForeignKey("Client.id"))


class ProductModel(Base):
    __tablename__ = "Product"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
