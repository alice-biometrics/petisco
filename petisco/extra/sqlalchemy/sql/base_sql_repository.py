from meiga import BoolResult, Error, Failure, isSuccess

from petisco import Uuid
from petisco.base.application.patterns.repository import Repository
from petisco.base.domain.errors.defaults.already_exists import (
    AggregateAlreadyExistError,
)
from petisco.base.domain.errors.defaults.not_found import (
    AggregateNotFoundError,
    AggregatesNotFoundError,
)


class BaseSqlRepository(Repository):
    @classmethod
    def fail_if_aggregate_already_exist(
        cls, model, aggregate_id: Uuid, result_error: Error = None
    ) -> BoolResult:
        if model:
            error = (
                AggregateAlreadyExistError(
                    aggregate_id, cls.__name__, model.__tablename__
                )
                if not result_error
                else result_error
            )
            return Failure(error)
        return isSuccess

    @classmethod
    def fail_if_aggregate_not_found(
        cls, model, aggregate_id: Uuid, result_error: Error = None
    ) -> BoolResult:
        if not model:
            error = (
                AggregateNotFoundError(aggregate_id, cls.__name__)
                if not result_error
                else result_error
            )
            return Failure(error)
        return isSuccess

    @classmethod
    def fail_if_aggregates_not_found(
        cls, model, result_error: Error = None
    ) -> BoolResult:
        if not model:
            error = (
                AggregatesNotFoundError(cls.__name__)
                if not result_error
                else result_error
            )
            return Failure(error)
        return isSuccess
