from meiga import BoolResult, Error, Failure, isSuccess

from petisco import Uuid
from petisco.base.application.patterns.repository import Repository
from petisco.extra.sqlalchemy.sql.errors import (
    EntitiesNotFoundError,
    EntityAlreadyExistError,
    EntityNotFoundError,
)


class BaseSqlRepository(Repository):
    @classmethod
    def fail_if_entity_already_exist(
        cls, model, entity_id: Uuid, result_error: Error = None
    ) -> BoolResult:
        if model:
            error = (
                EntityAlreadyExistError(cls.__name__, model.__tablename__, entity_id)
                if not result_error
                else result_error
            )
            return Failure(error)
        return isSuccess

    @classmethod
    def fail_if_entity_not_found(
        cls, model, entity_id: Uuid, result_error: Error = None
    ) -> BoolResult:
        if not model:
            error = (
                EntityNotFoundError(cls.__name__, entity_id)
                if not result_error
                else result_error
            )
            return Failure(error)
        return isSuccess

    @classmethod
    def fail_if_entities_not_found(
        cls, model, result_error: Error = None
    ) -> BoolResult:
        if not model:
            error = (
                EntitiesNotFoundError(cls.__name__)
                if not result_error
                else result_error
            )
            return Failure(error)
        return isSuccess
