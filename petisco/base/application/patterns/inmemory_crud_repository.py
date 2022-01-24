from typing import Any, Dict, List, Optional

from meiga import BoolResult, Error, Failure, Result, Success, isSuccess
from meiga.decorators import meiga

from petisco.base.application.patterns.crud_repository import (
    AggregateRootType,
    CrudRepository,
)
from petisco.base.application.patterns.transformer import Transformer
from petisco.base.domain.errors.defaults.already_exists import (
    AggregateAlreadyExistError,
)
from petisco.base.domain.errors.defaults.not_found import AggregateNotFoundError
from petisco.base.domain.model.uuid import Uuid


class InmemoryCrudRepository(CrudRepository[AggregateRootType]):
    def __init__(self, transformer: Optional[Transformer] = None):
        self._data: Dict[Uuid, Any] = dict()
        super().__init__(transformer)

    @meiga
    def save(self, aggregate_root: AggregateRootType) -> BoolResult:
        if aggregate_root.aggregate_id in self._data:
            return Failure(
                AggregateAlreadyExistError(aggregate_root.aggregate_id)
            )  # TODO: should we use AlreadyExist
        infrastructure_model = self.transformer.get_infrastructure_model(
            aggregate_root
        ).unwrap_or_return()
        self._data[aggregate_root.aggregate_id] = infrastructure_model
        return isSuccess

    @meiga
    def retrieve(self, aggregate_id: Uuid) -> Result[AggregateRootType, Error]:
        infrastructure_model = self._data.get(aggregate_id)
        if infrastructure_model is None:
            return Failure(
                AggregateNotFoundError(aggregate_id)
            )  # TODO: should we use NotFound
        aggregate_root = self.transformer.get_domain_model(
            infrastructure_model
        ).unwrap_or_return()
        return Success(aggregate_root)

    def update(self, aggregate_root: AggregateRootType) -> BoolResult:
        if aggregate_root.aggregate_id not in self._data:
            return Failure(
                AggregateNotFoundError(aggregate_root.aggregate_id)
            )  # TODO: should we use NotFound
        infrastructure_model = self.transformer.get_infrastructure_model(
            aggregate_root
        ).unwrap_or_return()
        self._data[aggregate_root.aggregate_id] = infrastructure_model
        return isSuccess

    def remove(self, aggregate_id: Uuid) -> BoolResult:
        if aggregate_id not in self._data:
            return Failure(
                AggregateNotFoundError(aggregate_id)
            )  # TODO: should we use NotFound
        self._data.pop(aggregate_id)
        return isSuccess

    def retrieve_all(self) -> Result[List[AggregateRootType], Error]:
        all = [
            self.transformer.get_domain_model(infrastructure_model).unwrap_or_return()
            for infrastructure_model in self._data.values()
        ]
        return Success(all)
