from pathlib import Path

import pytest

from petisco import AggregateRoot, DomainEvent, Uuid


class MyAggregateRootCreated(DomainEvent):
    pass


@pytest.mark.unit
class TestAggregateRoot:
    def should_return_success_result(self):  # noqa
        class MyAggregateRoot(AggregateRoot):
            name: str

            @staticmethod
            def create(name: str):
                aggregate_root = MyAggregateRoot(
                    aggregate_id=Uuid.from_value(
                        "0De49A24-C65A-4E8C-9917-125C067Eba2C"
                    ),
                    name=name,
                )
                aggregate_root.record(MyAggregateRootCreated())
                return aggregate_root

        aggregate_root = MyAggregateRoot.create(name="name")

        assert len(aggregate_root.pull_domain_events()) == 1
        assert aggregate_root.model_dump() == {
            "aggregate_id": "0De49A24-C65A-4E8C-9917-125C067Eba2C",
            "aggregate_version": 1,
            "name": "name",
        }

    def should_record_pull_and_clear_domain_events(self):  # noqa
        class MyAggregateRoot(AggregateRoot):
            name: str

        aggregate_root = MyAggregateRoot(
            aggregate_id=Uuid.from_value("0De49A24-C65A-4E8C-9917-125C067Eba2C"),
            name="name",
        )
        aggregate_root.record(MyAggregateRootCreated())

        assert len(aggregate_root.get_domain_events()) == 1
        assert len(aggregate_root.get_domain_events()) == 1

        assert len(aggregate_root.pull_domain_events()) == 1
        assert len(aggregate_root.pull_domain_events()) == 0

        aggregate_root = MyAggregateRoot(
            aggregate_id=Uuid.v4(),
            name="name",
        )
        assert len(aggregate_root.pull_domain_events()) == 0

    def should_encode_and_decode_complex_values(self):  # noqa
        class MyAggregateRoot(AggregateRoot):
            name: str

        aggregate_root = MyAggregateRoot(name="my-name")
        filename = ".tmp.json"
        path = Path(filename)
        path.write_text(aggregate_root.model_dump_json())
        aggregate_root_parsed = MyAggregateRoot.parse_file(filename)
        assert aggregate_root == aggregate_root_parsed
        path.unlink()

    def should_check_different_aggregate_id_with_different_instances(self):  # noqa
        class MyAggregateRoot(AggregateRoot):
            name: str

        instance_1 = MyAggregateRoot(name="instance_1")
        instance_2 = MyAggregateRoot(name="instance_1")

        assert instance_1.aggregate_id != instance_2.aggregate_id
