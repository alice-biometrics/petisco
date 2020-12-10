from abc import ABCMeta, abstractmethod

from meiga import (
    Result,
    Error,
    Failure,
    Success,
    NotImplementedMethodError,
    BoolResult,
    isSuccess,
)

from petisco.application.interface_repository import IRepository
from petisco.domain.value_objects.uuid import Uuid
from petisco.persistence.sql.errors import (
    ClientNotFoundError,
    EntityAlreadyExistError,
    EntityNotExistError,
    EntitiesNotExistError,
)


class SqlRepository(IRepository, metaclass=ABCMeta):
    def get_sql_internal_client_id(self, session, model) -> Result[int, Error]:
        if not hasattr(self, "internal_client_id"):
            internal_client_id = (
                session.query(model.id)
                .filter(model.client_id == self.get_client_id_value())
                .first()
            )
            if not internal_client_id:
                return Failure(ClientNotFoundError(self.get_client_id()))
            self.internal_client_id = internal_client_id.id

        return Success(self.internal_client_id)

    @classmethod
    def fail_if_entity_already_exist(cls, model, entity_id: Uuid) -> BoolResult:
        if model:
            return Failure(
                EntityAlreadyExistError(cls.__name__, model.__tablename__, entity_id)
            )
        return isSuccess

    @classmethod
    def fail_if_entity_not_exist(cls, model, entity_id: Uuid) -> BoolResult:
        if not model:
            return Failure(EntityNotExistError(cls.__name__, entity_id))
        return isSuccess

    @classmethod
    def fail_if_entities_not_exist(cls, model) -> BoolResult:
        if not model:
            return Failure(EntitiesNotExistError(cls.__name__))
        return isSuccess

    @abstractmethod
    def save(self, *args, **kwargs) -> BoolResult:
        return NotImplementedMethodError

    @abstractmethod
    def retrieve(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError

    @abstractmethod
    def retrieve_all(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError

    @abstractmethod
    def remove(self, *args, **kwargs) -> BoolResult:
        return NotImplementedMethodError
