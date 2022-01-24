import random

from petisco import AggregateRoot
from tests.modules.base.mothers.uuid_mother import UuidMother


class MyAggregateRoot(AggregateRoot):
    name: str


class MyAggregateRootMother:
    @staticmethod
    def any() -> MyAggregateRoot:
        return MyAggregateRoot(name="any", aggregate_id=UuidMother.any())

    @staticmethod
    def secondary() -> MyAggregateRoot:
        return MyAggregateRoot(name="secondary", aggregate_id=UuidMother.secondary())

    @staticmethod
    def random() -> MyAggregateRoot:
        name = "".join((random.choice("abcdxyzpqr") for i in range(5)))
        return MyAggregateRoot(name=name, aggregate_id=UuidMother.random())
