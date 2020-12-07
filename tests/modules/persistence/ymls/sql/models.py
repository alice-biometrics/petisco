from sqlalchemy import String, Integer, Column, Float
from petisco import Persistence

try:
    Base = Persistence.get_base("mysql_test")
except IndexError:
    Base = Persistence.get_base("sqlite_test")


class UserModel(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class ProductModel(Base):
    __tablename__ = "Product"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
