from typing import Any, Dict, List

from meiga import BoolResult, Error, Failure, Result, Success, isSuccess
from meiga.decorators import meiga

from petisco.base.application.patterns.crud_repository import (
    AggregateRootType,
    CrudRepository,
)
from petisco.base.domain.errors.defaults.already_exists import (
    AggregateAlreadyExistError,
)
from petisco.base.domain.errors.defaults.not_found import AggregateNotFoundError
from petisco.base.domain.model.uuid import Uuid


class InmemoryCrudRepository(CrudRepository[AggregateRootType]):
    def __init__(self):
        self._data: Dict[Uuid, Any] = dict()

    @meiga
    def save(self, aggregate_root: AggregateRootType) -> BoolResult:
        if aggregate_root.aggregate_id in self._data:
            return Failure(AggregateAlreadyExistError(aggregate_root.aggregate_id))
        self._data[aggregate_root.aggregate_id] = aggregate_root
        return isSuccess

    @meiga
    def retrieve(self, aggregate_id: Uuid) -> Result[AggregateRootType, Error]:
        aggregate_root = self._data.get(aggregate_id)
        if aggregate_root is None:
            return Failure(AggregateNotFoundError(aggregate_id))
        return Success(aggregate_root)

    def update(self, aggregate_root: AggregateRootType) -> BoolResult:
        if aggregate_root.aggregate_id not in self._data:
            return Failure(AggregateNotFoundError(aggregate_root.aggregate_id))
        self._data[aggregate_root.aggregate_id] = aggregate_root
        return isSuccess

    def remove(self, aggregate_id: Uuid) -> BoolResult:
        if aggregate_id not in self._data:
            return Failure(AggregateNotFoundError(aggregate_id))
        self._data.pop(aggregate_id)
        return isSuccess

    def retrieve_all(self) -> Result[List[AggregateRootType], Error]:
        return Success(list(self._data.values()))
