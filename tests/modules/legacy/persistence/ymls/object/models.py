from dataclasses import dataclass


@dataclass
class UserModel:
    name: str


@dataclass
class ProductModel:
    name: str
    price: float
