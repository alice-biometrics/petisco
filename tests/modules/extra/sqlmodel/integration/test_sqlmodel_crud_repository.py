import pytest
from meiga.assertions import assert_failure, assert_success

from petisco import (
    AggregateAlreadyExistError,
    AggregateNotFoundError,
    InmemoryCrudRepository,
)
from petisco.extra.sqlmodel.sqlmodel_crud_repository import SQLModelCrudRepository
from tests.modules.base.mothers.my_aggregate_mother import (
    MyAggregateRoot,
    MyAggregateRootMother,
)
from tests.modules.extra.sqlmodel.mother.infrastructure_model import InfrastructureModel


@pytest.mark.unit
@pytest.mark.skip
class TestSQLModelCrudRepository:
    repository: InmemoryCrudRepository
    aggregate_root: MyAggregateRoot

    def setup(self):
        self.repository = SQLModelCrudRepository[InfrastructureModel, MyAggregateRoot]()
        self.aggregate_root = MyAggregateRootMother.any()

    def _repository_with_aggregate_root(self):
        self.repository.save(self.aggregate_root)

    def _repository_with_n_aggregate_roots(self, number_of_aggregates: int):
        for _ in range(number_of_aggregates):
            self.repository.save(MyAggregateRootMother.random())

    def should_success_when_save(self):
        result = self.repository.save(self.aggregate_root)
        assert_success(result)

    def should_fail_when_save_and_already_exist(self):
        self._repository_with_aggregate_root()
        result = self.repository.save(self.aggregate_root)
        assert_failure(result, value_is_instance_of=AggregateAlreadyExistError)

    def should_success_when_retrieve(self):
        self._repository_with_aggregate_root()
        result = self.repository.retrieve(self.aggregate_root.aggregate_id)
        assert_success(
            result,
            value_is_instance_of=MyAggregateRoot,
            value_is_equal_to=self.aggregate_root,
        )

    def should_fail_when_retrieve_and_not_found(self):
        result = self.repository.retrieve(self.aggregate_root.aggregate_id)
        assert_failure(result, value_is_instance_of=AggregateNotFoundError)

    def should_success_when_update(self):
        self._repository_with_aggregate_root()
        self.aggregate_root.name = "other_name"
        result = self.repository.update(self.aggregate_root)
        assert_success(result)

    def should_fail_when_update_and_not_found(self):
        result = self.repository.update(self.aggregate_root)
        assert_failure(result, value_is_instance_of=AggregateNotFoundError)

    def should_success_when_retrieve_all(self):
        self._repository_with_aggregate_root()
        result = self.repository.retrieve_all()
        assert_success(
            result,
            value_is_instance_of=list,
            value_is_equal_to=[self.aggregate_root],
        )

    def should_success_when_retrieve_all_with_several_entries(self):
        self._repository_with_n_aggregate_roots(5)
        result = self.repository.retrieve_all()
        assert_success(
            result,
            value_is_instance_of=list,
        )
        assert len(result.unwrap()) == 5

    def should_success_when_retrieve_all_and_is_empty(self):
        self._repository_with_aggregate_root()
        result = self.repository.retrieve_all()
        assert_success(
            result,
            value_is_instance_of=list,
            value_is_equal_to=[],
        )

    def should_success_when_remove(self):
        self._repository_with_aggregate_root()
        result = self.repository.remove(self.aggregate_root.aggregate_id)
        assert_success(result)

    def should_fail_when_remove_and_not_found(self):
        result = self.repository.remove(self.aggregate_root.aggregate_id)
        assert_failure(result, value_is_instance_of=AggregateNotFoundError)
