from abc import abstractmethod
from typing import Generic, List, TypeVar

from meiga import BoolResult, Error, NotImplementedMethodError, Result

from petisco.base.application.patterns.repository import Repository
from petisco.base.domain.model.aggregate_root import AggregateRoot
from petisco.base.domain.model.uuid import Uuid

AggregateRootType = TypeVar("AggregateRootType", bound=AggregateRoot)


class CrudRepository(Generic[AggregateRootType], Repository):
    @abstractmethod
    def save(self, aggregate_root: AggregateRootType) -> BoolResult:
        return NotImplementedMethodError

    @abstractmethod
    def retrieve(self, aggregate_id: Uuid) -> Result[AggregateRootType, Error]:
        return NotImplementedMethodError

    @abstractmethod
    def update(self, aggregate_root: AggregateRootType) -> BoolResult:
        return NotImplementedMethodError

    @abstractmethod
    def remove(self, aggregate_id: Uuid) -> BoolResult:
        return NotImplementedMethodError

    @abstractmethod
    def retrieve_all(self) -> Result[List[AggregateRootType], Error]:
        return NotImplementedMethodError
