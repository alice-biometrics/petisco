from abc import ABCMeta, abstractmethod

from deprecation import deprecated
from meiga import (
    BoolResult,
    Error,
    Failure,
    NotImplementedMethodError,
    Result,
    Success,
    isSuccess,
)

from petisco import Uuid
from petisco.base.application.patterns.repository import Repository
from petisco.extra.sqlalchemy.sql.errors import (
    ClientNotFoundError,
    EntitiesNotFoundError,
    EntityAlreadyExistError,
    EntityNotFoundError,
    UserNotFoundError,
)


class SqlRepository(Repository, metaclass=ABCMeta):
    def get_sql_internal_client_id(self, session, model) -> Result[int, Error]:
        if not hasattr(self, "internal_client_id"):
            client_id = self.get_info_id().client_id
            internal_client_id = (
                session.query(model.id)
                .filter(model.client_id == client_id.value)
                .first()
            )
            if not internal_client_id:
                return Failure(ClientNotFoundError(client_id))
            self.internal_client_id = internal_client_id.id

        return Success(self.internal_client_id)

    def get_sql_internal_user_id(self, session, model) -> Result[int, Error]:
        if not hasattr(self, "internal_user_id"):
            user_id = self.get_info_id().user_id
            internal_user_id = (
                session.query(model.id).filter(model.user_id == user_id.value).first()
            )
            if not internal_user_id:
                return Failure(UserNotFoundError(user_id))
            self.internal_user_id = internal_user_id.id

        return Success(self.internal_user_id)

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

    @classmethod
    @deprecated("This method is deprecated. Please, use fail_if_entity_not_found")
    def fail_if_entity_not_exist(
        cls, model, entity_id: Uuid, result_error: Error = None
    ) -> BoolResult:
        return cls.fail_if_entity_not_found(model, entity_id, result_error)

    @classmethod
    @deprecated("This method is deprecated. Please, use fail_if_entities_not_found")
    def fail_if_entities_not_exist(
        cls, model, result_error: Error = None
    ) -> BoolResult:
        return cls.fail_if_entities_not_found(model, result_error)
