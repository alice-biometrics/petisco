import pytest

from petisco import DomainEvent, AggregateRoot, Uuid


class MyAggregateRootCreated(DomainEvent):
    pass


@pytest.mark.unit
def test_aggregate_root_should_return_success_result():
    class MyAggregateRoot(AggregateRoot):
        name: str

        @staticmethod
        def create(name: str):
            aggregate_root = MyAggregateRoot(
                aggregate_id=Uuid.from_value("0De49A24-C65A-4E8C-9917-125C067Eba2C"),
                name=name,
            )
            aggregate_root.record(MyAggregateRootCreated())
            return aggregate_root

    aggregate_root = MyAggregateRoot.create(name="name")

    assert len(aggregate_root.pull_domain_events()) == 1
    assert aggregate_root.dict() == {
        "aggregate_id": "0De49A24-C65A-4E8C-9917-125C067Eba2C",
        "aggregate_version": 1,
        "name": "name",
    }
