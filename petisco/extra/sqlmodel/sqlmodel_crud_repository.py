from abc import abstractmethod
from typing import Generic, List, TypeVar

from meiga import (
    BoolResult,
    Error,
    Failure,
    NotImplementedMethodError,
    Result,
    Success,
    isSuccess,
)
from meiga.decorators import meiga
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel, select

from petisco import Uuid
from petisco.base.application.patterns.crud_repository import (
    AggregateRootType,
    CrudRepository,
)
from petisco.base.domain.errors.defaults.already_exists import (
    AggregateAlreadyExistError,
)
from petisco.base.domain.errors.defaults.not_found import AggregateNotFoundError

engine = create_engine("sqlite:///database.db", echo=True)
SQLModel.metadata.create_all(engine)

SQLModelType = TypeVar("SQLModelType", bound=SQLModel)


class SQLModelCrudRepository(
    Generic[SQLModelType, AggregateRootType], CrudRepository[AggregateRootType]
):
    @abstractmethod
    def get_aggregate_root(
        self, sql_model: SQLModel
    ) -> Result[AggregateRootType, Error]:
        return NotImplementedMethodError

    @abstractmethod
    def get_sql_model(
        self, aggregate_root: AggregateRootType
    ) -> Result[SQLModel, Error]:
        return NotImplementedMethodError

    @abstractmethod
    def get_sql_model_type(self) -> SQLModelType:
        return NotImplementedMethodError

    @meiga
    def save(self, aggregate_root: AggregateRootType) -> BoolResult:

        with Session(engine) as session:
            model = self.get_sql_model_type()
            statement = select(model).where(
                model.aggregate_id == aggregate_root.aggregate_id.value
            )
            sql_model = session.exec(statement).first()
            if sql_model:
                return Failure(AggregateAlreadyExistError(aggregate_root.aggregate_id))

            sql_model = self.get_sql_model(aggregate_root).unwrap_or_return()

            session.add(sql_model)
            session.commit()

            return isSuccess

    @meiga
    def retrieve(self, aggregate_id: Uuid) -> Result[AggregateRootType, Error]:
        with Session(engine) as session:
            model = self.get_sql_model_type()
            statement = select(model).where(model.aggregate_id == aggregate_id.value)
            sql_model = session.exec(statement).first()
            if sql_model is None:
                return Failure(AggregateNotFoundError(aggregate_id))
            aggregate_root = self.get_aggregate_root(sql_model).unwrap_or_return()
            return Success(aggregate_root)

    def update(self, aggregate_root: AggregateRootType) -> BoolResult:
        with Session(engine) as session:
            model = self.get_sql_model_type()
            statement = select(model).where(
                model.aggregate_id == aggregate_root.aggregate_id.value
            )
            sql_model = session.exec(statement).first()
            if sql_model is None:
                return Failure(AggregateNotFoundError(aggregate_root.aggregate_id))

            sql_model = self.get_sql_model(aggregate_root)
            session.add(sql_model)
            session.commit()
            return isSuccess

    def remove(self, aggregate_id: Uuid) -> BoolResult:
        with Session(engine) as session:
            model = self.get_sql_model_type()
            statement = select(model).where(model.aggregate_id == aggregate_id.value)
            sql_model = session.exec(statement).first()
            if sql_model is None:
                return Failure(AggregateNotFoundError(aggregate_id))

            session.delete(sql_model)
            session.commit()

            return isSuccess

    def retrieve_all(self) -> Result[List[AggregateRootType], Error]:
        with Session(engine) as session:
            model = self.get_sql_model_type()
            statement = select(model)
            sql_models = session.exec(statement)

            all = [
                self.get_aggregate_root(sql_model).unwrap_or_return()
                for sql_model in sql_models
            ]
            return Success(all)
