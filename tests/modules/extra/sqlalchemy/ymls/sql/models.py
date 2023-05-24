from sqlalchemy import Column, Float, ForeignKey, Integer, String

from petisco import SqlBase


class ClientModel(SqlBase):
    __tablename__ = "Client"

    id = Column(Integer, primary_key=True)
    client_id = Column(String(36))
    name = Column(String(100), nullable=False)


class UserModel(SqlBase):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(36))
    name = Column(String(100), nullable=False)
    client_id = Column(Integer, ForeignKey("Client.id"))


class ProductModel(SqlBase):
    __tablename__ = "Product"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
