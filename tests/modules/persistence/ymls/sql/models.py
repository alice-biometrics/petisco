from sqlalchemy import String, Integer, Column, Float
from petisco import Persistence

Base = Persistence.get_base("sqlite_test")


class UserModel(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class ProductModel(Base):
    __tablename__ = "Product"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
